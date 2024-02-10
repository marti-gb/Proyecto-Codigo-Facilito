import mlflow
logged_model = 'runs:/1bc8633b52994925be677bc39643c7dd/model'
mlflow.set_tracking_uri("http://127.0.0.1:5000")
# Load model as a PyFuncModel.
model_name = "Modelo_Natalidad"
model_version = 3

# Cambia la carga del modelo a TensorFlow directamente
#tf_model = mlflow.tensorflow.load_model(model_uri=f"runs:/1bc8633b52994925be677bc39643c7dd/model")
loaded_model = mlflow.tensorflow.load_model(model_uri=f"models:/{model_name}/{model_version}")

# Predict on a Pandas DataFrame.
import pandas as pd
data = pd.read_csv("/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/Datos-Proyeccion-Natalidad-prediccion.csv")
xD = loaded_model.predict(pd.DataFrame(data))
print(xD)