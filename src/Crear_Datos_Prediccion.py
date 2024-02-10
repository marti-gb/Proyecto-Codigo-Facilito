import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import ElasticNet

def initial_model(directory_doc,name_doc,directory_proy):
    directory = directory_doc + name_doc
    dfDataDoc = pd.read_csv(directory)
    
    # Dividir los datos en características (X) y variable objetivo (y)
    nombres_columnas = dfDataDoc.columns.tolist()
    X = dfDataDoc[[nombres_columnas[0]]] # 'Año'
    y = dfDataDoc[nombres_columnas[1]] # 'Mundo'
    
    año_pred = X[nombres_columnas[0]].iloc[-1]
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    linear_reg, linear_mse = linear_regression(X_train, X_test, y_train, y_test)
    poly_reg, poly_mse = polynomial_regression(X_train, X_test, y_train, y_test)
    elastic_net, elastic_net_mse = elastic_regression(X_train, X_test, y_train, y_test)

    Mse_datos = {'Regresión': ['Lineal','Polinómica','Red Elastica'], 'MSE': [linear_mse,poly_mse,elastic_net_mse]}
    dfMse = pd.DataFrame(Mse_datos)
    
    model = select_model(directory_proy + name_doc.split('.')[0] + '-Predicciones.' + name_doc.split('.')[1], dfMse
                 , linear_reg, poly_reg, elastic_net, nombres_columnas, año_pred)
    
    return model

def linear_regression(X_train, X_test, y_train, y_test):  
    # Inicializar modelos de regresión lineal 
    linear_reg = LinearRegression()
    
    # Ajustar el modelo de regresión lineal
    linear_reg.fit(X_train, y_train)
    linear_pred = linear_reg.predict(X_test)
    linear_mse = mean_squared_error(y_test, linear_pred)

    return linear_reg, linear_mse
    
def polynomial_regression(X_train, X_test, y_train, y_test):
    # Inicializar modelos de regresión polinómica
    poly_reg = LinearRegression()
    
    # Ajustar el modelo de regresión polinómica
    poly_features = PolynomialFeatures(degree=2, include_bias= True)
    X_poly = poly_features.fit_transform(X_train)
    poly_reg.fit(X_poly, y_train)
    X_test_poly = poly_features.fit_transform(X_test)
    poly_pred = poly_reg.predict(X_test_poly)
    poly_mse = mean_squared_error(y_test, poly_pred)
    
    return poly_reg, poly_mse

def elastic_regression(X_train, X_test, y_train, y_test):
    elastic_net = ElasticNet(alpha = 0.1, l1_ratio = 0.5)

    # Ajustar el modelo de regresión red elástica
    elastic_net.fit(X_train, y_train)
    elastic_net_pred = elastic_net.predict(X_test)
    elastic_net_mse = mean_squared_error(y_test, elastic_net_pred)

    return elastic_net, elastic_net_mse

def select_model(directory_val_doc, mse, linear_reg, poly_reg, elastic_net, nombres_columnas, año_pred):
    dfMse_sort = mse.sort_values(by=['MSE'])
    Mse_sort= dfMse_sort.iloc[0][['Regresión', 'MSE']]
    
    lista_años = []  
    lista_pred = []
    
    # Comparar los errores cuadráticos medios para determinar el tipo de regresión
    if Mse_sort['Regresión'] == 'Lineal':
        print("El modelo de regresión lineal es más adecuado.")
        for _ in range(8):
            año_pred = año_pred + 1
            lista_años.append(año_pred)
        n_data = pd.DataFrame(lista_años)
        predictions = linear_reg.predict(n_data)
        lista_pred = predictions

        #print (predictions)
    
    if Mse_sort['Regresión'] == 'Polinómica':
        print("El modelo de regresión Polinómica es más adecuado.")
        poly_features = PolynomialFeatures(degree=2, include_bias= True)
        for _ in range(8):
            año_pred = año_pred + 1
            lista_años.append(año_pred)
        n_data = pd.DataFrame(lista_años)
        n_data_poly = poly_features.fit_transform(n_data)
        predictions = poly_reg.predict(n_data_poly)
        lista_pred = predictions
 
        #print (predictions)
    
    if Mse_sort['Regresión'] == 'Red Elastica':
        print("El modelo de regresión red elastica es más adecuado.")
        for _ in range(8):
            año_pred = año_pred + 1
            lista_años.append(año_pred)
        n_data = pd.DataFrame({nombres_columnas[0]:lista_años})
        predictions = elastic_net.predict(n_data)
        lista_pred = predictions
        
        #print (predictions)
    
    datos_pred = {nombres_columnas[0]: lista_años, nombres_columnas[1]: lista_pred}
    dfPred = pd.DataFrame(datos_pred)
    dfPred.to_csv(directory_val_doc, index=False, encoding='utf-8-sig')

    return dfPred

#linear_pred, linear_mse = initial_model('fd')
#print(linear_mse)
#initial_model('/Users/User/Desktop/Proyecto-CF/proyecto/data/','Alimentos.csv')