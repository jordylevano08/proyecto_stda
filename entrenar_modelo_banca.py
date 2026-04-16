import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Generar Datos Sintéticos de Banca
np.random.seed(42)
n_rows = 1500
data = {
    'ingresos': np.random.randint(1500, 15000, n_rows),
    'edad': np.random.randint(18, 75, n_rows),
    'puntuacion_crediticia': np.random.randint(300, 850, n_rows),
    'deudas_activas': np.random.randint(0, 10, n_rows),
    'antiguedad_laboral': np.random.randint(0, 40, n_rows)
}
df = pd.DataFrame(data)

# Crear regla de negocio para el "Riesgo" (Target)
# Si tiene baja puntuación y muchas deudas, el riesgo es alto (1)
df['target'] = ((df['puntuacion_crediticia'] < 500) & (df['deudas_activas'] > 4)).astype(int)

# 2. Entrenar el Modelo (Random Forest)
X = df.drop('target', axis=1)
y = df['target']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Guardar el modelo y los datos para Streamlit
with open('modelo_banca.pkl', 'wb') as f:
    pickle.dump(model, f)
df.to_csv('datos_banca.csv', index=False)

print("✅ Modelo entrenado y datos generados con éxito.")