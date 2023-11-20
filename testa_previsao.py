import requests
from datetime import datetime

input = {'DtEmissao':['2021-12-03'],
         'DtNascimento': ['1950-05-03'],
         'Sexo':['Masculino'],
         'CEP':[30672570]}
URL = 'https://ai.wiz.co/previsao' 
print(requests.post(URL,json=input,timeout=30).json())