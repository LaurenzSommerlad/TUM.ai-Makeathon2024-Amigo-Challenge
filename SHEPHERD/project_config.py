from pathlib import Path
import os

full_path = os.path.realpath(__file__)
path, _ = os.path.split(full_path)
PROJECT_DIR = Path(path)
CURR_KG = '8.9.21_kg'
KG_DIR = PROJECT_DIR / 'knowledge_graph' / CURR_KG
PREDICT_RESULTS_DIR = PROJECT_DIR / 'results'
SEED = 33

# Modify the following variables for your dataset
MY_DATA_DIR = Path("simulated_patients")
MY_TRAIN_DATA = MY_DATA_DIR / f"disease_split_train_sim_patients_{CURR_KG}.txt"
MY_VAL_DATA = MY_DATA_DIR / f"disease_split_val_sim_patients_{CURR_KG}.txt"
MY_TEST_DATA = MY_DATA_DIR / "PATH/TO/YOUR/DATA"
MY_SPL_DATA = MY_DATA_DIR / "PATH/TO/YOUR/DATA" # Result of data_prep/shortest_paths/add_spl_to_patients.py (suffix: _spl_matrix.npy)
MY_SPL_INDEX_DATA = MY_DATA_DIR / "PATH/TO/YOUR/DATA" # Result of data_prep/shortest_paths/add_spl_to_patients.py (suffix: _spl_index_dict.pkl)