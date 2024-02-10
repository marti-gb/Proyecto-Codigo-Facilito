import luigi
import pandas as pd
import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from Consolidado_datos import consolidar_datos, predicciones_datos
import modelo as mod

rdData = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/'
rdModel = '/Users/User/Desktop/Proyecto-CF/proyecto/models/'
n_Data = 'Datos-Proyeccion-Natalidad.csv'
n_Data_predict = 'Datos-Proyeccion-Natalidad-prediccion.csv'
n_model = 'mejor_modelo.h5'
n_data_test = 'prepared_data.npz'

n_Data_copy = 'Datos-Proyeccion-Natalidad_copia.csv'
n_Data_predict_copy = 'Datos-Proyeccion-Natalidad-prediccion_copia.csv'
n_model_copy = 'mejor_modelo_copia.h5'
n_model_copy2 = 'mejor_modelo_copia2.h5'

class Funcion1Task(luigi.Task):
    def output(self):
        return luigi.LocalTarget(rdData + n_Data)
        
    def run(self):
        # Lógica de la primera función
        print("Ejecutando Funcion 1")
        consolidar_datos()

class Funcion2Task(luigi.Task):
    def requires(self):
        return Funcion1Task()
    
    def output(self):
        return luigi.LocalTarget(rdData + n_Data_predict)
        
    def run(self):
        # Lógica de la segunda función
        print("Ejecutando Funcion 2")
        predicciones_datos()
        

class Funcion3Task(luigi.Task):
    def requires(self):
        return Funcion2Task()
    
    def output(self):
        return luigi.LocalTarget(rdData + n_Data)
    
    def run(self):
        # Lógica de la tercera función
        print("Ejecutando Funcion 3")
    
class Funcion4Task(luigi.Task):
    def requires(self):
        return Funcion3Task()
    def output(self):
        return luigi.LocalTarget(rdData + n_data_test)

    def run(self):
        # Lógica de la tercera función
        print("Ejecutando Funcion 4")
        X_train, X_test, y_train, y_test = mod.preparar_data_model(rdData, n_Data, n_Data_predict, rdModel, n_model)
        np.savez(self.output().path, x_train=X_train, x_test=X_test, y_train=y_train, y_test=y_test)

class Funcion5Task(luigi.Task):
    def requires(self):
        return Funcion4Task()

    def output(self):
        return luigi.LocalTarget(rdModel + n_model)
    
    def run(self):
        import mlflow

        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        mlflow.set_experiment("/Mode_natalidad/Natalidad")
        with mlflow.start_run() as run:       
            # Lógica de la tercera función
            print("Ejecutando Funcion 5")
            print(self.input().path)
            data_train = np.load(self.input().path)
            x_train, x_test, y_train, y_test = data_train['x_train'], data_train['x_test'], data_train['y_train'], data_train['y_test']

            model = mod.crear_model()
            mod.entrena_model(model, x_train, x_test, y_train, y_test, rdModel, n_model, 'R')
            
            model_uri = f"runs:/{run.info.run_id}/Modelo_Natalidad" 
            model_uri = "runs:/{}/Modelo_Natalidad".format(run.info.run_id)
            #dfData = pd.DataFrame.from_dict(data_train)
            loaded_model = load_model(self.output().path)
            
            #mlflow.tensorflow.log_model(loaded_model, artifact_path="model")
            
            data = np.load(rdData + n_data_test)
            x_train, x_test, y_train, y_test = data['x_train'], data['x_test'], data['y_train'], data['y_test']        
            train_model = mod.evaluar_model(x_test, y_test, rdModel, n_model, 'R')
            mlflow.tensorflow.log_model(train_model, "Modelo_Natalidad" #, artifact_path="model"
                                       )
            
            mlflow.log_table(data = pd.DataFrame.from_dict(data_train['x_train']), artifact_file="data_xtrain.json")
            mlflow.log_table(data = pd.DataFrame.from_dict(data_train['x_test']), artifact_file="data_xtest.json")
            mlflow.log_table(data = pd.DataFrame.from_dict(data_train['y_train']), artifact_file="data_ytrain.json")
            mlflow.log_table(data = pd.DataFrame.from_dict(data_train['y_test']), artifact_file="data_ytest.json")
            mlflow.log_artifact(self.input().path)
            mlflow.register_model(model_uri, 'Modelo_Natalidad')
        
class Funcion6Task(luigi.Task):
    def requires(self):
        return Funcion5Task()

    def output(self):
        return luigi.LocalTarget(rdModel + n_model)

    def run(self):     
        print("Ejecutando Funcion 6")
        data = np.load(rdData + n_data_test)
        x_train, x_test, y_train, y_test = data['x_train'], data['x_test'], data['y_train'], data['y_test']        
        train_model = mod.evaluar_model(x_test, y_test, rdModel, n_model, '')


class Funcion7Task(luigi.Task):
    if os.path.exists(rdData + n_Data):
        if os.path.exists(rdData + n_Data_copy):
             os.remove(rdData + n_Data_copy)
        shutil.copy2(rdData + n_Data, rdData + n_Data_copy)
        
    if os.path.exists(rdData + n_Data_predict):
        if os.path.exists(rdData + n_Data_predict_copy):
            os.remove(rdData + n_Data_predict_copy)
        shutil.copy2(rdData + n_Data_predict, rdData + n_Data_predict_copy)
        
    if os.path.exists(rdModel + n_model):
        if os.path.exists(rdData + n_model_copy):
            os.remove(rdModel + n_model_copy)
        shutil.copy2(rdModel + n_model, rdModel + n_model_copy)
    
    def output(self):
        return luigi.LocalTarget(rdModel + n_model_copy2)
        
    def run(self): 
        print("Ejecutando Funcion 7")
        b_model = True
        b_nData = True
        model = ''
        new_data = ''
        if os.path.exists(rdModel + n_model_copy):
            model = load_model(rdModel + n_model_copy)
            shutil.copy2(rdModel + n_model_copy, rdModel + n_model_copy2)
        else:
            b_model = False
        if os.path.exists(rdData + n_Data_predict_copy):
            new_data = pd.read_csv(rdData + n_Data_predict_copy)
            nuevos_nombres = {'Año': 'Anho', 'FPI (Nominal)': 'FPI_Nominal','Precio Brent':'Precio_Brent'
                      ,'Mundo (Inflacion)':'Inflacion_Mundial','Mundo (Natalidad)':'Natalidad_Mundial'}
            new_data.rename(columns = nuevos_nombres,inplace=True)
        else:
            b_nData = False

        if b_model and b_nData:
            print("------------------------")
            print("Proyección de Natalidad:")
            predicciones = mod.predicc_model(model, new_data)
            print(predicciones)
            new_data['Mundo (Natalidad)'] = predicciones
            print(new_data)
            print("------------------------")
            print()
        else:
            print("-----------------------------------------------------------------------------------------------------")
            print("No se puede dar una proyección de la Natalidad a falta del modelo entrenado y/o datos para proyección")
            print("-----------------------------------------------------------------------------------------------------")
            print()

class Ejecutar_Funcion(luigi.Task):
    funcion = luigi.Parameter()

    def requires(self):
        if self.funcion == 'M':
            return Funcion6Task()
        if self.funcion == 'P':
            return Funcion7Task()
            
    def run(self): 
        print("Fin Ejecutar_Funcion")
        
         
if __name__ == '__main__':
 
    if os.path.exists(rdData + n_Data):
        os.remove(rdData + n_Data)
    if os.path.exists(rdData + n_Data_predict):
        os.remove(rdData + n_Data_predict)
    if os.path.exists(rdModel + n_model):
        os.remove(rdModel + n_model)
    if os.path.exists(rdData + n_data_test):
        os.remove(rdData + n_data_test)
    if os.path.exists(rdModel + n_model_copy2):
        os.remove(rdModel + n_model_copy2)
    #luigi.build([Funcion3Task()], local_scheduler=True)
    #luigi.build([Funcion5Task()], local_scheduler=True)
    
    #luigi.build([Funcion6Task()], local_scheduler=True)
    #luigi.build([Funcion7Task()], local_scheduler=True)

    luigi.run()
