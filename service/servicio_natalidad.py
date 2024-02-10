import bentoml
import numpy as np
from pandas import json_normalize
from bentoml.io import PandasDataFrame, NumpyNdarray, JSON

MODEL_TAG = "modelo_natalidad:3"

Modelo_Natalidad_m = bentoml.tensorflow.get(MODEL_TAG)
Modelo_Natalidad_m_runner = Modelo_Natalidad_m.to_runner()

Modelo_Natalidad_m_service = bentoml.Service(
    "servicio_modelo_natalidad", runners=[Modelo_Natalidad_m_runner]
)

@Modelo_Natalidad_m_service.api(input=JSON(), output=JSON())
def predict(input_df):
    df = json_normalize(input_df)
    print(df)
    pr = Modelo_Natalidad_m_runner.run(df)
    df1 = pr.to_json(orient='records')
    return df1#Modelo_Natalidad_m_runner.run(df)
