import requests
from datetime import datetime

input = {'DtEmissao':['2021-12-03'],
         'DtNascimento': ['1950-05-03'],
         'Sexo':['Feminino'],
         'CEP':[30672570]}
URL = 'http://172.17.0.2:9696/previsao' #mudar depois pra url de produção
print(requests.post(URL,json=input,timeout=30).json())