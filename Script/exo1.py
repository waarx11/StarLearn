# Traitement des valeurs manquantes
import pandas as pd
import numpy as np
import pickle
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Charger le fichier CSV dans un dataframe

df = pd.read_csv('File/exoplanets.csv')


#  On traite les valeurs manquantes et les colonnes inutiles
df.dropna( how='all', axis=1, inplace=True)  # On supprime les colonnes contenant que des valeurs manquantes
df.drop(columns=["kepid","kepoi_name","kepler_name", "koi_pdisposition","koi_tce_delivname"], inplace=True) # On supprime les colonnes inutiles

df.dropna(inplace=True) # On supprime les lignes contenant des valeurs manquantes


### Traitement des données 
# On transforme les valeurs de la colonne koi_disposition en entier
df["koi_disposition"] = df["koi_disposition"].map(
    {"CONFIRMED": 1, "FALSE POSITIVE": 0, "CANDIDATE": 2}
)

cols_to_scale = df.drop(["koi_disposition", "koi_fpflag_nt", "koi_fpflag_ss", "koi_fpflag_co", "koi_fpflag_ec"], axis=1).columns

scaler = MinMaxScaler()
df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

with open('SiteWeb/ia/minMaxScaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)



for i in df.columns :
    break
    print(i)
    # print(df[i])
    if df[i].dtype == "float64" :
        print("Min : ", df[i].min())
        print("Max : ", df[i].max())
        print("Moyenne : ", df[i].mean())
        print("1er quartile : ", df[i].quantile(0.25))
        print("Médiane : ", df[i].median())
        print("3ème quartile : ", df[i].quantile(0.75))
    else :
        print("### Pas un float ###")
    print()

# Diviser le dataset en training en test set
X = df.drop('koi_disposition', axis=1)
y = df['koi_disposition']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Echantillonnage dans le cas de classes déséquilibrées (undersampling)
print("Nombre d'occurence dans chaque classe (avant undersampling): ", sorted(Counter(y_train).items()))
# Randomly under sample the majority class
rus = RandomUnderSampler(random_state=42)
X_train_rus, y_train_rus= rus.fit_resample(X_train, y_train)
# Check the number of records after under sampling
print("Nombre d'occurence dans chaque classe (après undersampling): ", sorted(Counter(y_train_rus).items()))
# print(X_train_rus,y_train_rus)

datasetFinal = X_train_rus
datasetFinal['koi_disposition'] = y_train_rus
# Mélanger les lignes
datasetFinal = datasetFinal.sample(frac=1, random_state=np.random.seed(42))
# print(datasetFinal)

# Exporter le nouveau dataset au format csv
datasetFinal.to_csv('File/exoplanetsExo1.csv', index=False)

datasetFinalTest = X_train_rus
datasetFinalTest['koi_disposition'] = y_train_rus
# Mélanger les lignes
datasetFinalTest = datasetFinalTest.sample(frac=1, random_state=np.random.seed(42))
# print(datasetFinalTest)

# Exporter le nouveau dataset au format csv
datasetFinalTest.to_csv('File/exoplanetsExo1Test.csv', index=False)