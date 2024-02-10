import polars as pl
import pandas as pd

def Data_Food(directory_doc, directory_data_doc, name_doc):
    directory = directory_doc + name_doc
    dfFood = pl.read_excel(directory
                        ,xlsx2csv_options={"skip_empty_lines": False}
                        ,read_csv_options={"has_header": False
                                           , "new_columns": ['Año','FPI (Nominal)', 'FPI(Real)']
                                           ,"columns": [0,1,2]
                                          , "skip_rows" : 4
                                          }
                      )  
    dfFood = dfFood.drop_nulls()
    dPFood = dfFood.drop("FPI(Real)").to_pandas()
    dPFood.to_csv(directory_data_doc + name_doc.split('.')[0] + '-Datos.csv', index=False, encoding='utf-8-sig')
    
    return dPFood

#Data_Food('/Users/User/Desktop/Proyecto-CF/proyecto/data/Indice_Precio_Alimentos/', '/Users/User/Desktop/Proyecto-CF/proyecto/data/', 'food_price_index_nominal_real.xlsx')