from neo4j import GraphDatabase
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer



def fetch_data(session, query):
    result = session.run(query)
    data = []
    for record in result:
        subject_id = record['subject_id']
        disease_status = record['disease']
        phenotype = record['phenotypes']
        protein = record['proteins']
        data.append({"subject_id": subject_id,"pheno_type":phenotype,"protien":protein, "disease": disease_status})
    data = pd.DataFrame(data)
    json_output = data.rename(columns={'subject_id': 'id', 'phenotypes': 'positive_phenotypes', 'disease': 'true_diseases'}).to_json(orient='records', indent=4)
    return json_output,data

def main(type=1):

    uri = "bolt://83.229.84.12:7687"  
    username = "tumaiReadonly"
    password = "MAKEATHON2024"  
    database = "graph2.db"
    AUTH = (username, password)

    with GraphDatabase.driver(uri, auth=AUTH) as driver:
        driver.verify_connectivity()
    if type==0:
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
    if type==1:
        query = """
        MATCH (b:Biological_sample)-[:HAS_DISEASE]->(d:Disease)
        WHERE NOT d.name = 'control'
        OPTIONAL MATCH (b)-[:HAS_PROTEIN]->(p:Protein)
        OPTIONAL MATCH (b)-[:HAS_PHENOTYPE]->(ph:Phenotype)
        WITH b, 
            collect(DISTINCT p.id) AS proteins,
            collect(DISTINCT ph.id) AS phenotypes,
            d.synonyms AS synonyms
        UNWIND synonyms AS synonym
        WITH b, proteins, phenotypes, synonym
        WHERE synonym CONTAINS 'ICD10CM:'
        RETURN b.subjectid AS subject_id, 
            proteins,
            phenotypes,
            substring(synonym, size('ICD10CM:'), 1) AS disease
    """
    with driver.session(database=database) as session:
        jsondata,data = fetch_data(session, query)
        
    return jsondata,data





def process_data(data):
    mlb_pheno = MultiLabelBinarizer()
    mlb_protein = MultiLabelBinarizer()
    pheno_encoded = mlb_pheno.fit_transform(data['pheno_type'])
    protein_encoded = mlb_protein.fit_transform(data['protien'])
    df_pheno_encoded = pd.DataFrame(pheno_encoded, columns=mlb_pheno.classes_)
    df_protein_encoded = pd.DataFrame(protein_encoded, columns=mlb_protein.classes_)
    df_final = pd.concat([data[['subject_id']], df_pheno_encoded, data['disease']], axis=1)
    # df_final = pd.concat([data[['subject_id']], df_pheno_encoded, df_protein_encoded, data['disease']], axis=1)
    return df_final