import requests
from datetime import datetime

input = {'DtEmissao':'2021-04-03',
         'DtNascimento': '1970-05-03',
         'Sexo':'Masculino',
         'CEP':70855080}
URL = 'http://10.12.0.186:9696/previsao' #mudar depois pra url de produção
print(requests.post(URL,json=input,timeout=30).json())