from FeatureCloud.app.engine.app import AppState, app_state, Role
import time
import os
import logging

from neo4j import GraphDatabase, Query, Record
from neo4j.exceptions import ServiceUnavailable
from pandas import DataFrame

from utils import read_config,write_output

from FeatureCloud.app.engine.app import AppState, app_state

import numpy as np
import torch
from run import main
import pandas as pd

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
        
        """
        with driver.session(database=database) as session:
	data = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType;")
	edge_types = [r["relationshipType"] for r in data]
        """
        edge_types = request(
            "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType;",
            lambda data: [r["relationshipType"] for r in data]
        )
        assert edge_types

        edges = []

        """
        t = edge_types.index("HAS_DISEASE")
with driver.session(database=database) as session:
	data = session.run("MATCH (a:Biological_sample)-[r:HAS_DISEASE]->(b) RETURN id(a), id(b)")
	patients = list(set(r["id(a)"] for r in data))
	edges += [(r["id(a)"], t, r["id(b)"]) for r in data]
"""
        t = edge_types.index("HAS_DISEASE")
        data = request(
            "MATCH (a:Biological_sample)-[r:HAS_DISEASE]->(b) RETURN id(a), id(b)",
            lambda data: [(r["id(a)"], r["id(b)"]) for r in data]
        )
        assert data
        patients = set(r[0] for r in data)
        diseases = set(r[1] for r in data)
        with_disease = [(r[0], t, r[1]) for r in data]
        edges += with_disease

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
        all_patients = set(r[0] for r in delta)
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

        logger.info(f"{edges.__len__(), len(patients)}")

        complex_format = np.array(edges)
        kge_model, entity_encoder, relation_encoder = main(complex_format)

        to_check = all_patients.difference(patients)
        d_n = len(diseases)
        r_emb = np.tile(
            relation_encoder.transform([edge_types.index("HAS_DISEASE")])[0],
            (d_n, 1)
        )
        d_emb = np.concatenate([entity_encoder.transform([disease])[0] for disease in diseases], axis=0)

        results = []
        for patient in to_check:
            p_emb = np.tile(
                entity_encoder.transform([patient])[0],
                (d_n, 1)
            )
            inp = torch.from_numpy(np.concatenate([p_emb, r_emb, d_emb], axes=1))
            res = kge_model(inp)
            max_res = torch.argmax(res).detach().numpy()
            disease = diseases[max_res]
            results.append((patient, disease))
        
        df = pd.DataFrame(results, columns=["subject_id", "disease"])
        logging.info(df.to_csv())

        return 'terminal'