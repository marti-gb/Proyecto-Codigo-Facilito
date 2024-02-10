import polars as pl
import pandas as pd

def Data_Natalidad(directory_doc, directory_data_doc, name_doc):
    directory = directory_doc + name_doc
    dfNatalidad = pl.read_csv(directory,skip_rows=4,truncate_ragged_lines=True)
    dfNatalidad2 = dfNatalidad.clone()

    colname=dfNatalidad2.select(['Country Name']).transpose().to_numpy()
    colcode=dfNatalidad2.select(['Country Code']).transpose().to_numpy()
    
    ListName = []
    for name, code in zip(colname[0].tolist(), colcode[0].tolist()):
        if (name == ''):
        	ListName.append(code)
        else:
            ListName.append(name)
    
    dfNatalidad2 = dfNatalidad2.drop('Country Name','Country Code','Country Code')
    dfNat = dfNatalidad2.transpose(include_header=True,header_name="Year",column_names=ListName)
    dfNat2=dfNat.with_columns([
        (pl.col('AFE').alias("África oriental y meridional")),
        (pl.col('AFW').alias("África occidental y central")),
    ])
    dfNat2 = dfNat2.drop('AFE','AFW')
    
    dfNat3 = dfNat2.to_pandas()
    dfNat3.drop([0,1,64],axis=0,inplace=True)
    dfNat3 = dfNat3.replace({"": 0})
    dfNat3=dfNat3.astype("float32")
    dfNat3['Year'] = dfNat3['Year'].astype(int)
    
    dfNat3 = dfNat3[['Year', 'Mundo']]
    is_zero = dfNat3.loc[:, 'Mundo'] > 0
    dfNat3 = dfNat3.loc[is_zero]

    dfNat3 = dfNat3.rename(columns={ 'Year': 'Año',  'Mundo': 'Mundo (Natalidad)'})
    dfNat3.to_csv(directory_data_doc + name_doc.split('.')[0] + '-Datos.' + name_doc.split('.')[1], index=False, encoding='utf-8-sig')
    
    return dfNat3

#Data_Natalidad('/Users/User/Desktop/Proyecto-CF/proyecto/data/Natalidad/', '/Users/User/Desktop/Proyecto-CF/proyecto/data/', 'natalidad.csv')