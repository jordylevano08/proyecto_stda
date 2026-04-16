import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Generar datos ficticios
np.random.seed(42)
df = pd.DataFrame({
    'ingresos': np.random.randint(1000, 20000, 1000),
    'edad': np.random.randint(18, 85, 1000),
    'puntuacion_crediticia': np.random.randint(300, 850, 1000),
    'deudas_activas': np.random.randint(0, 15, 1000),
    'antiguedad_laboral': np.random.randint(0, 50, 1000)
})
df['target'] = ((df['puntuacion_crediticia'] < 500) & (df['deudas_activas'] > 5)).astype(int)

# 2. Entrenar modelo
X, y = df.drop('target', axis=1), df['target']
modelo = RandomForestClassifier().fit(X, y)

# 3. Guardar el archivo PKL
with open('modelo_banca.pkl', 'wb') as f:
    pickle.dump(modelo, f)

print("✅ Archivo 'modelo_banca.pkl' creado con éxito.")