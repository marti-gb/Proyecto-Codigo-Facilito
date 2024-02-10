import polars as pl
import pandas as pd
import numpy as np

def Data_Brent(directory_doc, directory_data_doc, name_doc):
    directory = directory_doc + name_doc
    dfBrent = pl.read_excel(directory, sheet_name='Data'
                        ,xlsx2csv_options={"skip_empty_lines": False}
                        ,read_csv_options={"has_header": False
                                           , "new_columns": ['Null','Año', 'Precio Brent']
                                           , "skip_rows" : 3
                                          }
                            )
    dfBrent = dfBrent.drop("Null")
    dPBrent = dfBrent.to_pandas()
    dPBrent.to_csv(directory_data_doc + name_doc.split('.')[0] + '-Datos.csv', index=False, encoding='utf-8-sig')
    
    return dPBrent
    
#Data_Brent('/Users/User/Desktop/Proyecto-CF/proyecto/data/Brent/', '/Users/User/Desktop/Proyecto-CF/proyecto/data/', 'brent-crude-oil-price-annually-1976-2023.xlsx')