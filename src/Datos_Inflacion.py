import polars as pl
import pandas as pd

def Data_Inflacion(directory_doc, directory_data_doc, name_doc):
    directory = directory_doc + name_doc
    dfInflacion = pl.read_csv(directory,skip_rows=4,truncate_ragged_lines=True)
    
    dfInflacion2 = dfInflacion.clone()
    colnameInf=dfInflacion2.select(['Country Name']).transpose().to_numpy()
    colcodeInf=dfInflacion2.select(['Country Code']).transpose().to_numpy()
    
    ListName = []
    for name, code in zip(colnameInf[0].tolist(), colcodeInf[0].tolist()):
        if (name == ''):
        	ListName.append(code)
        else:
            ListName.append(name)
    
    dfInflacion2 = dfInflacion2.drop('Country Name','Country Code')
    dfInf = dfInflacion2.transpose(include_header=True,header_name="Year",column_names=ListName)
    
    dfInf2=dfInf.with_columns([
        (pl.col('AFE').alias("África oriental y meridional")),
        (pl.col('AFW').alias("África occidental y central")),
    ])
    dfInf2 = dfInf2.drop('AFE','AFW')
    dfInf3 = dfInf2.to_pandas()
    
    dfInf3.drop([0,1],axis=0,inplace=True)
    dfInf3 = dfInf3.replace({"": 0})
    dfInf3=dfInf3.astype("float32")
    dfInf3['Year'] = dfInf3['Year'].astype(int)
    
    dfInf3 = dfInf3[['Year', 'Mundo']]
    is_zero = dfInf3.loc[:, 'Mundo'] > 0
    dfInf3 = dfInf3.loc[is_zero]
    
    dfInf3 = dfInf3.rename(columns={ 'Year': 'Año',  'Mundo': 'Mundo (Inflacion)'})
    dfInf3.to_csv(directory_data_doc + name_doc.split('.')[0] + '-Datos.' + name_doc.split('.')[1], index=False, encoding='utf-8-sig')
    
    return dfInf3

#Data_Inflacion('/Users/User/Desktop/Proyecto-CF/proyecto/data/Inflacion/', '/Users/User/Desktop/Proyecto-CF/proyecto/data/', 'inflacion.csv')