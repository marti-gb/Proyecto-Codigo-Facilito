from metaflow import FlowSpec, step

class NatalidadFlow(FlowSpec):
    rdData = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/'
    rdModel = '/Users/User/Desktop/Proyecto-CF/proyecto/models/'
    n_Data = 'Datos-Proyeccion-Natalidad.csv'
    n_Data_predict = 'Datos-Proyeccion-Natalidad-prediccion.csv'
    n_model = 'mejor_modelo.h5'
    
    @step
    def start(self):
        # Inicialización del flujo
        print("Iniciando el flujo...")
        self.next(self.prepare_data)

    @step
    def prepare_data(self):
        # Aquí puedes incluir la lógica para preparar tus datos
        import Consolidado_datos as conData
        print("Preparando datos...")
        conData.consolidar_datos()
        self.next(self.prepare_data_predict)

    @step
    def prepare_data_predict(self):
        # Aquí puedes incluir la lógica para preparar tus datos
        import Consolidado_datos as conData
        print("Preparando datos para predicción...")
        conData.predicciones_datos()
        self.next(self.train_model)

    @step
    def prepare_data_predict(self):
        # Aquí puedes incluir la lógica para preparar tus datos
        import modelo as mod
        print("Preparando modelado de datos...")
        X_train, X_test, y_train, y_test = mod.preparar_data_model(rdData, n_Data, n_Data_predict, '', '')
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.next(self.train_eval_model)
        
    @step
    def train_eval_model(self):
        # Configuración y entrenamiento del modelo de TensorFlow
        import modelo as mod
        print("Configurando y entrenando el modelo...")
        model = mod.crear_model()
        entrena_model(model, self.X_train, self.X_test, self.y_train, self.y_test, rdModel, n_model)
        save_model = mod.evaluar_model(self.X_test, self.y_test)
        self.save_model = save_model
        self.next(self.predict_model)
    @step
    def predict_model(self):
        # Configuración y entrenamiento del modelo de TensorFlow
        import pandas as pd
        import modelo as mod
        print("Configurando y entrenando el modelo...")
        new_data = pd.read_csv(rdData + n_Data_predict)
        predictions = mod.predicc_model(self.save_model, new_data)
        print(predictions)
        
        self.next(self.end)
    @step
    def end(self):
        # Tarea final del flujo
        print("Flujo completado.")

if __name__ == '__main__':
    NatalidadFlow()
