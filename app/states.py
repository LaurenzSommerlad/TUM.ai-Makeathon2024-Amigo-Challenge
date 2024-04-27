from FeatureCloud.app.engine.app import AppState, app_state, Role
import time
import os
import logging

from neo4j import GraphDatabase, Query, Record
from neo4j.exceptions import ServiceUnavailable
from pandas import DataFrame

from utils import read_config,write_output

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from FeatureCloud.app.engine.app import AppState, app_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = read_config()

@app_state('initial')
class ExecuteState(AppState):

    def register(self):
        self.register_transition('terminal', Role.BOTH)

        
    def run(self):
        
        # Get Neo4j credentials from config
        # print("Gotten to credentials part")

        neo4j_credentials = config.get("neo4j_credentials", {})
        NEO4J_URI = neo4j_credentials.get("NEO4J_URI", "")
        NEO4J_USERNAME = neo4j_credentials.get("NEO4J_USERNAME", "")
        NEO4J_PASSWORD = neo4j_credentials.get("NEO4J_PASSWORD", "")
        NEO4J_DB = neo4j_credentials.get("NEO4J_DB", "")
        logger.info(f"Neo4j Connect to {NEO4J_URI} using {NEO4J_USERNAME}")
        
        # Driver instantiation
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

        query ="""
    MATCH (b:Biological_sample)
    OPTIONAL MATCH (b)-[:HAS_PROTEIN]->(p:Protein)
    OPTIONAL MATCH (b)-[:HAS_PHENOTYPE]->(ph:Phenotype)
    OPTIONAL MATCH (b)-[:HAS_DISEASE]->(d:Disease)
    RETURN b.subjectid AS subject_id, 
        collect(DISTINCT p.id) AS proteins,
        collect(DISTINCT ph.id) AS phenotypes,
        CASE WHEN d.name = 'control' THEN 0 ELSE 1 END AS disease
        """
        
        df = None

        with driver.session(database=NEO4J_DB) as session: 
            result = session.run(query)

            data = []
            for record in result:
                subject_id = record['subject_id']
                disease_status = record['disease']
                phenotype = record['phenotypes']
                protein = record['proteins']
                data.append({"subject_id": subject_id,"pheno_type":phenotype,"protien":protein, "disease": disease_status})
            
            df = DataFrame(data)
            logger.info(f"Constructed a DataFrame of shape {df.shape}")
        driver.close()

        logger.info(df.head())
            
        mlb_pheno = MultiLabelBinarizer()
        mlb_protein = MultiLabelBinarizer()
        pheno_encoded = mlb_pheno.fit_transform(df['pheno_type'])
        protein_encoded = mlb_protein.fit_transform(df['protien'])
        df_pheno_encoded = pd.DataFrame(pheno_encoded, columns=mlb_pheno.classes_)
        df_protein_encoded = pd.DataFrame(protein_encoded, columns=mlb_protein.classes_)
        df_final = pd.concat([df[['subject_id']], df_pheno_encoded, df['disease']], axis=1)

        df = df_final
        X = df.drop(['subject_id', 'disease'], axis=1)
        y = df['disease']

        classifier = RandomForestClassifier(n_estimators=3, random_state=42)

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        classifier.fit(X_train, y_train)
        logger.info("Model finished training")

        # Predict the test set
        y_pred = classifier.predict(X_test)

        y_pred = classifier.predict(X_test)
        results_df = pd.DataFrame({
            'subject_id': X_test.index,  # or X_test['subject_id'] if 'subject_id' is a column
            'disease': y_pred
        })
        results_df.to_csv('predictions.csv')

        logger.info(classification_report(y_test, y_pred))
        logger.info(f"Accuracy: {accuracy_score(y_test, y_pred)}")

        return 'terminal'