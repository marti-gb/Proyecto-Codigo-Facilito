import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import mlflow

def preparar_data_model(directory_data, name_doc_data, name_doc_data_pred, directory_model, name_model):
    #Cargar los datos en un data frame
    #data = pd.read_csv('/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/Datos-Proyeccion-Natalidad.csv') 
    data = pd.read_csv(directory_data + name_doc_data) 
    #new_data = pd.read_csv('/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/Datos-Proyeccion-Natalidad-prediccion.csv')
    #new_data = pd.read_csv(directory_data + name_doc_data_pred)
    nuevos_nombres = {'Año': 'Anho', 'FPI (Nominal)': 'FPI_Nominal','Precio Brent':'Precio_Brent'
                      ,'Mundo (Inflacion)':'Inflacion_Mundial','Mundo (Natalidad)':'Natalidad_Mundial'}
    data.rename(columns = nuevos_nombres,inplace=True)
    # Dividir los datos en características (X) y etiquetas (y)
    X = data.iloc[:, 0:4]  # Primeras cuatro columnas como características
    y = data.iloc[:, 4:]    # Última columna como etiqueta
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    return X_train, X_test, y_train, y_test

#Crear el modelo de red neuronal
def crear_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(300, input_dim=4, activation= 'relu'),
        tf.keras.layers.Dense(300, activation= 'relu'),
        tf.keras.layers.Dense(300, activation= 'relu'),
        tf.keras.layers.Dense(300, activation= 'relu'),
        tf.keras.layers.Dense(1)
    ])

    # Compilar el modelo
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    
    return model

# Entrenar el modelo
def entrena_model(model, X_train, X_test, y_train, y_test, directory_model, name_model, register):
    checkpoint_vmae = ModelCheckpoint(directory_model + name_model #'/Users/User/Desktop/Proyecto-CF/proyecto/models/mejor_modelo.h5'
                                        , monitor='val_mae', save_best_only=True, mode='min')
    model.fit(X_train, y_train, epochs=4093, batch_size=32, validation_data=(X_test, y_test), callbacks=[checkpoint_vmae], verbose=0)

    if register == 'R':
        mlflow.log_param('epochs', 4093)
        mlflow.log_param('optimizer', 'adam') #optimizer='adam', loss='mean_squared_error', metrics=['mae']
        mlflow.log_param('loss', 'mean_squared_error')
        mlflow.log_param('metrics', 'mae')
        mlflow.log_param('callbacks', 'checkpoint_vmae')
        mlflow.log_param('callbacks_monitor', 'val_mae')
        mlflow.log_param('callbacks_save', 'save_best_only')
        mlflow.log_param('callbacks_save_mode', 'min')


def evaluar_model(X_test, y_test, directory_model, name_model, register):
    save_model = load_model(directory_model + name_model)
    loss_eval, val_mae = save_model.evaluate(X_test, y_test)
    print(f'Loss: {loss_eval}, MAE: {val_mae}')
    if register == 'R':
        metrics = {
                "Eval_accuracy": val_mae,
                "Eval_loss": loss_eval
                }

        mlflow.log_metrics(metrics)
        
    return save_model

def predicc_model(model, new_data):
    predictions = model.predict(new_data)
    return predictions

#preparar_data_model('','','')