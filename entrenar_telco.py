import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Datos de ejemplo: Meses contrato, Factura, Reclamos
data = {
    'meses': [1, 24, 12, 2, 36, 5],
    'factura': [100, 50, 80, 110, 40, 95],
    'reclamos': [3, 0, 1, 4, 0, 2],
    'se_va': [1, 0, 0, 1, 0, 1] # 1 = Se fuga
}
df = pd.DataFrame(data)
modelo = RandomForestClassifier().fit(df.drop('se_va', axis=1), df['se_va'])

with open('modelo_telco.pkl', 'wb') as f:
    pickle.dump(modelo, f)