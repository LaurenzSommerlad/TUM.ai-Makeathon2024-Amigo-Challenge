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
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from FeatureCloud.app.engine.app import AppState, app_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

old_logger_i = logger.info
old_logger_e = logger.error

def new_logger_i(msg):
    with open("./i_log.txt", "a") as f:
        f.write(f"{msg}\n")
    old_logger_i(msg)

def new_logger_e(msg):
    with open("./e_log.txt", "a") as f:
        f.write(f"{msg}\n")
    old_logger_e(msg)

logger.info = new_logger_i
logger.error = new_logger_e

config = read_config()
neo4j_credentials = config.get("neo4j_credentials", {})
NEO4J_URI = neo4j_credentials.get("NEO4J_URI", "")
NEO4J_USERNAME = neo4j_credentials.get("NEO4J_USERNAME", "")
NEO4J_PASSWORD = neo4j_credentials.get("NEO4J_PASSWORD", "")
NEO4J_DB = neo4j_credentials.get("NEO4J_DB", "")
logger.info(f"Neo4j Connect to {NEO4J_URI} using {NEO4J_USERNAME}")

def request(query, parse_func):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    with driver.session(database=NEO4J_DB) as session: 
        try:
            ret = parse_func(session.run(query))
            logger.info(query)
            return ret
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
        finally:
            driver.close()

@app_state('initial')
class ExecuteState(AppState):

    def register(self):
        self.register_transition('terminal', Role.BOTH)

        
    def run(self):
        ## Retriving Phenotypes
        pheno_data = request("""
MATCH (:Biological_sample)-[:HAS_PHENOTYPE]->(ph:Phenotype)
RETURN DISTINCT ph.id AS phenotype
""", lambda data: [r["phenotype"] for r in data])
        assert pheno_data
        mlb_pheno = MultiLabelBinarizer()
        mlb_pheno.fit_transform(pheno_data)
        
        
        # Get Neo4j credentials from config
        # print("Gotten to credentials part")
        
        # Driver instantiation

        # Get Neo4j credentials from config
        # print("Gotten to credentials part")
        
        # Driver instantiation
        
        delta_test = request(
            """
MATCH (b:Biological_sample)
WHERE NOT (b:Biological_sample)-[:HAS_DISEASE]->()
OPTIONAL MATCH (b:Biological_sample)-[:HAS_PHENOTYPE]->(ph:Phenotype)
RETURN b.subjectid as subject_id, collect(DISTINCT ph.id) AS phenotypes

""",
            lambda data: [{
                "subject_id": r["subject_id"], 
                "pheno_type": r["phenotypes"]
            } for r in data]
        ) 
        
        data_test = pd.DataFrame(delta_test)
        df_pheno_encoded_test = pd.DataFrame(data_test['pheno_type'], columns=mlb_pheno.classes_)
        df_final_test = pd.concat([data_test[['subject_id']], df_pheno_encoded_test], axis=1)
        df_test = df_final_test
        X_test = df_test.drop(['subject_id'], axis=1)
        
        ## TYPE 1
        delta = request(
            """
MATCH (b:Biological_sample)-[:HAS_DISEASE]->(d:Disease)
        WHERE NOT d.name = 'control'
        OPTIONAL MATCH (b)-[:HAS_PHENOTYPE]->(ph:Phenotype)
        WITH b,
            collect(DISTINCT ph.id) AS phenotypes,
            d.synonyms AS synonyms
        UNWIND synonyms AS synonym
        WITH b, phenotypes, synonym
        WHERE synonym CONTAINS 'ICD10CM:'
        RETURN b.subjectid AS subject_id,
            phenotypes,
            substring(synonym, size('ICD10CM:'), 1) AS disease

""",
            lambda data: [{
                "subject_id": r["subject_id"], 
                "disease": r["disease"],
                "pheno_type": r["phenotypes"]
            } for r in data]
        )

        data = pd.DataFrame(delta)
        df_pheno_encoded = pd.DataFrame(data['pheno_type'], columns=mlb_pheno.classes_)
        df_final = pd.concat([data[['subject_id']], df_pheno_encoded, data['disease']], axis=1)
    
        logging.info("Data processed")
        df = df_final
        X = df.drop(['subject_id', 'disease'], axis=1)
        y = df['disease']
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)
        classifier = RandomForestClassifier(n_estimators=3, random_state=42)
        classifier.fit(X, y)

        # Split the data
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # classifier.fit(X_train, y_train)
        logger.info("Model finished training")
        # Predict the test set
        y_pred = classifier.predict(X_test)
        
        
        results_df = pd.DataFrame({
            'subject_id': X_test.index,  # or X_test['subject_id'] if 'subject_id' is a column
            'disease': y_pred
        })
        logger.info(results_df.to_csv())
        results_df.to_csv('./predictions_B.csv')

        # logger.info(classification_report(y_test, y_pred))
        # logger.info(f"Accuracy: {accuracy_score(y_test, y_pred)}")

        ## TYPE 0
        logger.info("Doing type 1 now")

        delta = request(
            """
MATCH (b:Biological_sample)
    OPTIONAL MATCH (b)-[:HAS_PHENOTYPE]->(ph:Phenotype)
    OPTIONAL MATCH (b)-[:HAS_DISEASE]->(d:Disease)
    RETURN b.subjectid AS subject_id,
        collect(DISTINCT ph.id) AS phenotypes,
        CASE WHEN d.name = 'control' THEN 0 ELSE 1 END AS disease
""",
            lambda data: [{
                "subject_id": r["subject_id"], 
                "disease": r["disease"],
                "pheno_type": r["phenotypes"]
            } for r in data]
        )

        data = pd.DataFrame(delta)

        #mlb_pheno = MultiLabelBinarizer()
        pheno_encoded = mlb_pheno.fit_transform(data['pheno_type'])
        df_pheno_encoded = pd.DataFrame(pheno_encoded, columns=mlb_pheno.classes_)
        df_final = pd.concat([data[['subject_id']], df_pheno_encoded, data['disease']], axis=1)

        logging.info("Data processed")

        df = df_final
        X = df.drop(['subject_id', 'disease'], axis=1)
        y = df['disease']

        classifier = RandomForestClassifier(n_estimators=3, random_state=42)

        # # Split the data
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        classifier.fit(X, y)
        # classifier.fit(X_train, y_train)
        logger.info("Model finished training")

        # Predict the test set
        y_pred = classifier.predict(X_test)
        y_pred = classifier.predict(X_test)
        results_df = pd.DataFrame({
            'subject_id': X_test.index,  # or X_test['subject_id'] if 'subject_id' is a column
            'disease': y_pred
        })
        results_df.to_csv('./predictions_A.csv')

        logger.info(classification_report(y_test, y_pred))
        logger.info(f"Accuracy: {accuracy_score(y_test, y_pred)}")

        return 'terminal'