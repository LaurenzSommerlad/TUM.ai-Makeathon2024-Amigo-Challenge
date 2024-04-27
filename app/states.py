from FeatureCloud.app.engine.app import AppState, app_state, Role
import time
import os
import logging

from neo4j import GraphDatabase, Query, Record
from neo4j.exceptions import ServiceUnavailable, SessionError
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

def run_query(session, query: str):
    try:
        return session.run(query)
    except (ServiceUnavailable, SessionError) as e:
        logger.error("Failed to connect to the database")
        logger.info(query)
        logger.error(str(e))
        return None

@app_state('initial')
class ExecuteState(AppState):

    def register(self):
        self.register_transition('terminal', Role.BOTH)

        
    def run(self):
        # Get Neo4j credentials from config
        neo4j_credentials = config.get("neo4j_credentials", {})
        NEO4J_URI = neo4j_credentials.get("NEO4J_URI", "")
        NEO4J_USERNAME = neo4j_credentials.get("NEO4J_USERNAME", "")
        NEO4J_PASSWORD = neo4j_credentials.get("NEO4J_PASSWORD", "")
        NEO4J_DB = neo4j_credentials.get("NEO4J_DB", "")
        logger.info(f"Neo4j Connect to {NEO4J_URI} using {NEO4J_USERNAME}")

        # Driver instantiation
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

        # Create a driver session with defined DB
        with driver.session(database=NEO4J_DB) as session:

            # Example Query to Count Nodes 
            node_count_query = "MATCH (n) RETURN count(n)"

            # Use .data() to access the results array        
            results = session.run(node_count_query).data()
            logger.info(results)

        write_output(f"{results}")

        # Close the driver connection
        driver.close()

        return 'terminal'