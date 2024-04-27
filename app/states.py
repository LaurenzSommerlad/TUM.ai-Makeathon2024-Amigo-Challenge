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
            return parse_func(session.run(query))
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
        
        # Get Neo4j credentials from config
        # print("Gotten to credentials part")
        
        # Driver instantiation
        

        edge_types = request(
            "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType;",
            lambda data: [r["relationshipType"] for r in data]
        )
        assert edge_types

        """
        t = edge_types.index("HAS_DISEASE")
with driver.session(database=database) as session:
	data = session.run("MATCH (a:Biological_sample)-[r:HAS_DISEASE]->(b) RETURN id(a), id(b)")
	patients = list(set(r["id(a)"] for r in data))
	edges += [(r["id(a)"], t, r["id(b)"]) for r in data]
        """
        edges = []
        t = edge_types.index("HAS_DISEASE")
        delta = request(
            "MATCH (a:Biological_sample)-[r:HAS_DISEASE]->(b) RETURN id(a), id(b)",
            lambda data: [(r["id(a)"], t, r["id(b)"]) for r in data]
        )
        assert delta
        patients = list(set(r[0] for r in delta))
        edges += delta

        """
        t = edge_types.index("HAS_PROTEIN")
with driver.session(database=database) as session:
	data = session.run("MATCH (a:Biological_sample)-[r:HAS_PROTEIN]->(b) RETURN id(a), id(b)")
	edges += [(r["id(a)"], t, r["id(b)"]) for r in data]
        """
        t = edge_types.index("HAS_PROTEIN")
        delta = request(
            "MATCH (a:Biological_sample)-[r:HAS_PROTEIN]->(b) RETURN id(a), id(b)",
            lambda data: [(r["id(a)"], t, r["id(b)"]) for r in data]
        )
        assert delta
        edges += delta

        """
        t = edge_types.index("HAS_PHENOTYPE")
with driver.session(database=database) as session:
	data = session.run("MATCH (a:Biological_sample)-[r:HAS_PHENOTYPE]->(b) RETURN id(a), id(b)")
	edges += [(r["id(a)"], t, r["id(b)"]) for r in data]
        """
        t = edge_types.index("HAS_PHENOTYPE")
        delta = request(
            "MATCH (a:Biological_sample)-[r:HAS_PHENOTYPE]->(b) RETURN id(a), id(b)",
            lambda data: [(r["id(a)"], t, r["id(b)"]) for r in data]
        )
        assert delta
        edges += delta

        logger.info(f"{edges.__len__()}, {patients.__len__()}")


        return 'terminal'