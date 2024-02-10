import pandas as pd
import os
import Datos_Alimento as al
import Datos_Brent as br
import Datos_Inflacion as inf
import Datos_Natalidad as nat
import Crear_Datos_Prediccion as pred


rdConsolidado = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Consolidado/'
rdProcesado = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Datos_Procesados/'
rdProyeccion = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Datos_Proyectados/'
rdAlimentos = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Indice_Precio_Alimentos/'
rdBrent = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Brent/'
rdInflacion = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Inflacion/'
rdNatalidad = '/Users/User/Desktop/Proyecto-CF/proyecto/data/Natalidad/'
n_Consolidado = 'Datos-Proyeccion-Natalidad.csv'
n_Consolidado_test = 'Datos-Proyeccion-Natalidad-prediccion.csv'

def obtener_nombres_por_extension(ruta_directorio, extension, nombre_archivo):
    # Obtener todos los archivos en el directorio
    archivos_en_directorio = os.listdir(ruta_directorio)
    
    # Filtrar archivos por la extensión y obtener solo los nombres
    if len(nombre_archivo) == 0:
        archivo = [archivo.split('.')[0] for archivo in archivos_en_directorio if archivo.endswith(extension)]
    else:
        archivo = [archivo.split('.')[0] for archivo in archivos_en_directorio if nombre_archivo in archivo and archivo.endswith(extension)]
        
    return archivo

def consolidar_datos():
    n_Food = obtener_nombres_por_extension(rdAlimentos, 'xlsx', '')
    n_Brent = obtener_nombres_por_extension(rdBrent, 'xlsx', '')
    n_Inflacion = obtener_nombres_por_extension(rdInflacion, 'csv', '')
    n_Natalidad = obtener_nombres_por_extension(rdNatalidad, 'csv', '')

    dfFood = al.Data_Food(rdAlimentos, rdProcesado, n_Food[0] + '.xlsx')
    dfBrent = br.Data_Brent(rdBrent, rdProcesado, n_Brent[0] + '.xlsx')
    dfInflacion = inf.Data_Inflacion(rdInflacion, rdProcesado, n_Inflacion[0] + '.csv')
    dfNatalidad = nat.Data_Natalidad(rdNatalidad, rdProcesado, n_Natalidad[0] + '.csv')

    dfCons_Food_Brent = pd.merge(dfFood,  dfBrent, on ='Año', how='inner')
    dfCons_Inflacion_Natalidad = pd.merge(dfInflacion,  dfNatalidad, on ='Año', how='inner')
    dfCons_Total = pd.merge(dfCons_Food_Brent,  dfCons_Inflacion_Natalidad, on ='Año', how='inner')
    
    dfCons_Total.to_csv(rdConsolidado + n_Consolidado, index=False, encoding='utf-8-sig')

def predicciones_datos():
    n_Food = obtener_nombres_por_extension(rdProcesado, 'csv', 'food')
    n_Brent = obtener_nombres_por_extension(rdProcesado, 'csv', 'brent')
    n_Inflacion = obtener_nombres_por_extension(rdProcesado, 'csv', 'inflacion') 
    
    print("Datos: " + n_Food[0])
    dfFood = pred.initial_model(rdProcesado, n_Food[0] + '.csv', rdProyeccion)
    print("Datos: " + n_Brent[0])
    dfBrent = pred.initial_model(rdProcesado, n_Brent[0] + '.csv', rdProyeccion)
    print("Datos: " + n_Inflacion[0])
    dfInflacion = pred.initial_model(rdProcesado, n_Inflacion[0] + '.csv', rdProyeccion)

    dfCons_Food_Brent = pd.merge(dfFood,  dfBrent, on ='Año', how='inner')
    dfCons_Food_Brent_Inflacion = pd.merge(dfCons_Food_Brent,  dfInflacion, on ='Año', how='inner')
    nombres_columnas_pred_consolidado = dfCons_Food_Brent_Inflacion.columns.tolist()
    año_inicial_pred_consolidado = dfCons_Food_Brent_Inflacion[nombres_columnas_pred_consolidado[0]].iloc[0]
    
    dfConsolidado = pd.read_csv(rdConsolidado + n_Consolidado)
    nombres_columnas_consolidado = dfConsolidado.columns.tolist()
    año_final_consolidado = dfConsolidado[nombres_columnas_consolidado[0]].iloc[-1]

    dfPFood = pd.read_csv(rdProcesado + n_Food[0] + '.csv')
    nombres_columnas_alimentos = dfPFood.columns.tolist()
    año_final_alimentos = dfPFood[nombres_columnas_alimentos[0]].iloc[-1]

    dfPBrent = pd.read_csv(rdProcesado + n_Brent[0] + '.csv')
    nombres_columnas_brent = dfPBrent.columns.tolist()
    año_final_brent = dfPBrent[nombres_columnas_brent[0]].iloc[-1]

    dfPInflacion = pd.read_csv(rdProcesado + n_Inflacion[0] + '.csv')
    nombres_columnas_inflacion = dfPInflacion.columns.tolist()
    año_final_inflacion = dfPInflacion[nombres_columnas_inflacion[0]].iloc[-1]

    dfPredFood = ''
    if año_final_consolidado < año_final_alimentos:
        lista_años = []
        lista_pred = []
        año = año_final_consolidado
        
        for _ in range(año_final_alimentos - año_final_consolidado):
            año = año + 1
            registro = dfPFood.loc[dfPFood[nombres_columnas_alimentos[0]] == año]
            lista_años.append(registro[nombres_columnas_alimentos[0]].iloc[0])
            lista_pred.append(registro[nombres_columnas_alimentos[1]].iloc[0])
        
        datos_pred_Food = {nombres_columnas_alimentos[0]: lista_años, nombres_columnas_alimentos[1]: lista_pred}
        dfPredFood = pd.DataFrame(datos_pred_Food)
        #print(dfPredFood)

    dfPredBrent = ''
    if año_final_consolidado < año_final_brent:
        lista_años = []
        lista_pred = []
        año = año_final_consolidado
        
        for _ in range(año_final_brent - año_final_consolidado):
            año = año + 1
            registro = dfPBrent.loc[dfPBrent[nombres_columnas_brent[0]] == año]
            lista_años.append(registro[nombres_columnas_brent[0]].iloc[0])
            lista_pred.append(registro[nombres_columnas_brent[1]].iloc[0])
        
        datos_pred_Brent = {nombres_columnas_brent[0]: lista_años, nombres_columnas_brent[1]: lista_pred}
        dfPredBrent = pd.DataFrame(datos_pred_Brent)
        #print(dfPredBrent)

    dfPredInflacion = ''
    if año_final_consolidado < año_final_inflacion:
        lista_años = []
        lista_pred = []
        año = año_final_consolidado
        
        for _ in range(año_final_inflacion - año_final_consolidado):
            año = año + 1
            registro = dfPInflacion.loc[dfPInflacion[nombres_columnas_inflacion[0]] == año]
            lista_años.append(registro[nombres_columnas_inflacion[0]].iloc[0])
            lista_pred.append(registro[nombres_columnas_inflacion[1]].iloc[0])
        
        datos_pred_Inflacion = {nombres_columnas_inflacion[0]: lista_años, nombres_columnas_inflacion[1]: lista_pred}
        dfPredInflacion = pd.DataFrame(datos_pred_Inflacion)
        #print(dfPredInflacion)
    
    dfConsPred_Food_Brent_Inflacion = ''
    
    if len(dfPredFood) == len (dfPredBrent) and len(dfPredFood) == len (dfPredInflacion):
        dfConsPred_Food_Brent = pd.merge(dfPredFood,  dfPredBrent, on ='Año', how='inner')
        dfConsPred_Food_Brent_Inflacion = pd.merge(dfConsPred_Food_Brent,  dfPredInflacion, on ='Año', how='inner')
    
    elif len(dfPredFood) == len (dfPredBrent):
        dfConsPred_Food_Brent = pd.merge(dfPredFood,  dfPredBrent, on ='Año', how='inner')
        nombres_columnas_pred_Food_Brent = dfConsPred_Food_Brent.columns.tolist()
        año_final_pred_pred_Food_Brent = dfConsPred_Food_Brent[nombres_columnas_pred_Food_Brent[0]].iloc[-1]

        if len(dfPredInflacion) < len (dfConsPred_Food_Brent):
            nombres_columnas_pred_inflacion = dfPredInflacion.columns.tolist()
            año_final_pred_inflacion = dfPredInflacion[nombres_columnas_pred_inflacion[0]].iloc[-1]
            
            lista_años = []
            lista_pred = []
            
            for _ in range(año_final_pred_pred_Food_Brent - año_final_pred_inflacion):
                año_final_pred_inflacion = año_final_pred_inflacion + 1
                registro = dfInflacion.loc[dfInflacion[nombres_columnas_inflacion[0]] == año_final_pred_inflacion]
                lista_años.append(registro[nombres_columnas_inflacion[0]].iloc[0])
                lista_pred.append(registro[nombres_columnas_inflacion[1]].iloc[0])
                
            ad_datos_pred_Inflacion = {nombres_columnas_inflacion[0]: lista_años, nombres_columnas_inflacion[1]: lista_pred}
            df_ad_datos_pred_Inflacion = pd.concat([dfPredInflacion, pd.DataFrame(ad_datos_pred_Inflacion)], ignore_index=True)

        dfConsPred_Food_Brent_Inflacion = pd.merge(dfConsPred_Food_Brent,  df_ad_datos_pred_Inflacion, on ='Año', how='inner')

    if len(dfConsPred_Food_Brent_Inflacion) > 0:
        dfCons_Food_Brent_Inflacion = pd.concat([dfConsPred_Food_Brent_Inflacion, dfCons_Food_Brent_Inflacion], ignore_index=True)

    print(dfCons_Food_Brent_Inflacion)
    dfCons_Food_Brent_Inflacion.to_csv(rdConsolidado + n_Consolidado_test, index=False, encoding='utf-8-sig')
    
#consolidar_datos()