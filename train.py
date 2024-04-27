
from dataprocess import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

type = 1
json_data,data = main(type=type)

df = process_data(data)
# df.head()


X = df.drop(['subject_id', 'disease'], axis=1)
y = df['disease']
if type==1:
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)


classifier = RandomForestClassifier(n_estimators=3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
classifier.fit(X_train, y_train)


# Predict the test set
y_pred = classifier.predict(X_test)
results_df = pd.DataFrame({   
    'subject_id': X_test.index,  
    'disease': y_pred
})
if type==0:
    results_df.to_csv('taskA_predictions.csv')
else:
    results_df.to_csv('taskB_predictions.csv')
# print(classification_report(y_test, y_pred))
# print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
