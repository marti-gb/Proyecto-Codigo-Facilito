import bentoml
import mlflow
import tensorflow as tf
import pandas as pd

mlflow.set_tracking_uri("http://127.0.0.1:5000")

model_name = "Modelo_Natalidad"
model_version = 3

# Cambia la carga del modelo a TensorFlow directamente
#tf_model = mlflow.tensorflow.load_model(model_uri=f"runs:/1bc8633b52994925be677bc39643c7dd/model")
tf_model = mlflow.tensorflow.load_model(model_uri=f"models:/{model_name}/{model_version}")

# Guarda el modelo en BentoML
bento_model = bentoml.tensorflow.save_model(f"{model_name}:{model_version}", tf_model)
