import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import joblib
import os

# Get the absolute path of the ml_model directory
ml_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml_model'))

# read and shuffle the dataset
df = pd.read_csv('../data/dataset.csv')
df = shuffle(df, random_state=42)
df.head()

# remove hyphen from strings
for col in df.columns:
    df[col] = df[col].str.replace('_', ' ')
df.head()

# dataset characteristics
df.describe()

# checking for null and NaN values
null_checker = df.apply(lambda x: sum(x.isnull())).to_frame(name='count')

# remove trailing spaces from the symptom columns
cols = df.columns
data = df[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df.shape)

df = pd.DataFrame(s, columns=df.columns)
df.head()

# fill Nan with zeros
df = df.fillna(0)
df.head()

# symptom severity rank
df1 = pd.read_csv('../data/Symptom-severity.csv')
df1['Symptom'] = df1['Symptom'].str.replace('_', ' ')
df1.head()

df1['Symptom'].unique()

# encode symptoms with the symptom rank
vals = df.values
symptoms = df1['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = df1[df1['Symptom'] == symptoms[i]]['weight'].values[0]

d = pd.DataFrame(vals, columns=cols)
d.head()

# assign symptoms with no rank to 0
d = d.replace('dischromic  patches', 0)
d = d.replace('spotting  urination', 0)
df = d.replace('foul smell of urine', 0)
df.head(10)

# check if entire columns have zero values so we can drop those values
null_checker = df.apply(lambda x: sum(x.isnull())).to_frame(name='count')

# get names of diseases from the data
df['Disease'].unique()

# select the features as symptoms column and label as Disease column
data = df.iloc[:, 1:].values
labels = df['Disease'].values

x_train, x_test, y_train, y_test = train_test_split(data, labels, train_size=0.8, random_state=42)
# print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# #random forest model
rfc = RandomForestClassifier(random_state=42)
rnd_forest = RandomForestClassifier(random_state=42, max_features='sqrt', n_estimators=500, max_depth=13)
rnd_forest.fit(x_train, y_train)
# preds=rnd_forest.predict(x_test)
# print(x_test[0])
# print(preds[0])
# conf_mat = confusion_matrix(y_test, preds)
# df_cm = pd.DataFrame(conf_mat, index=df['Disease'].unique(), columns=df['Disease'].unique())
# print('F1-score% =', f1_score(y_test, preds, average='macro')*100, '|', 'Accuracy% =', accuracy_score(y_test, preds)*100)
# sns.heatmap(df_cm)
# #save the random forest model
# joblib.dump(rfc, "random_forest.joblib")

discrp = pd.read_csv("../data/symptom_Description.csv")
discrp.head()

ektra7at = pd.read_csv("../data/symptom_precaution.csv")
ektra7at.head()

loaded_rf = joblib.load(os.path.join(ml_model_path, 'random_forest.joblib'))


def predd(x, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17):
    psymptoms = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17]
    # print(psymptoms)
    a = np.array(df1["Symptom"])
    b = np.array(df1["weight"])
    for j in range(len(psymptoms)):
        for k in range(len(a)):
            if psymptoms[j] == a[k]:
                psymptoms[j] = b[k]
    psy = [psymptoms]
    pred2 = x.predict(psy)
    disp = discrp[discrp['Disease'] == pred2[0]]
    disp = disp.values[0][1]
    recommend = ektra7at[ektra7at['Disease'] == pred2[0]]
    c = np.where(ektra7at['Disease'] == pred2[0])[0][0]
    precaution_list = []
    for lists in range(1, len(ektra7at.iloc[c])):
        precaution_list.append(ektra7at.iloc[c, lists])
    print("The Disease Name: ", pred2[0])
    print("The Disease Description: ", disp)
    print("Recommended Things to do at home: ")
    for lists in precaution_list:
        print(lists)


sympList = df1["Symptom"].to_list()
print(sympList);
for index, item in enumerate(sympList):
    print(f"{index}: {item}")

# predicting
predd(rnd_forest, sympList[0], sympList[25], sympList[85], sympList[28], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
