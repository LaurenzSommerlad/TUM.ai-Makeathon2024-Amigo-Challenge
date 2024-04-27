import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

val_path = 'disease_split_val_sim_patients_8.9.21_kg.txt'
vdata=[]
with open(val_path, 'r') as file:
    for line in file:
        # Parse the JSON data from each line
        json_data = json.loads(line)
        vdata.append(json_data)

val_df = pd.DataFrame(vdata)
val_df = val_df[(val_df['age'] == 'Onset_Infant') | (val_df['age'] == 'Onset_Child')]
df = val_df[['true_genes','positive_phenotypes','true_diseases']]
df= df.explode('true_diseases')

mlb_genes = MultiLabelBinarizer()
genes_encoded = mlb_genes.fit_transform(df['true_genes'])

mlb_phenotypes = MultiLabelBinarizer()
phenotypes_encoded = mlb_phenotypes.fit_transform(df['positive_phenotypes'])

# Create feature DataFrame from encoded data
features = pd.DataFrame(genes_encoded, columns=mlb_genes.classes_)
phenotypes_df = pd.DataFrame(phenotypes_encoded, columns=mlb_phenotypes.classes_)
features = pd.concat([features, phenotypes_df], axis=1)
labels = df['true_diseases']


# Split data into training and testing sets
features_subset = features.iloc[:9000]
labels_subset = labels.iloc[:9000]

# Now use train_test_split on this subset
X_train, X_test, y_train, y_test = train_test_split(features_subset, labels_subset, test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")
f1 = f1_score(y_test, y_pred, average='macro')
print(f"Test F1 Score: {f1:.4f}")

