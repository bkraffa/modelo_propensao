import pickle5 as pickle
import pandas as pd
from unidecode import unidecode
from datetime import datetime
from flask import Flask,request,jsonify

with open('objetos/custom_transformer_pickle.pkl', 'rb') as file:
    column_trans = pickle.load(file)

with open('objetos/modelo_rfc.pkl', 'rb') as file:
    rfc = pickle.load(file)

def prepara_features(input):
    input = request.get_json()
    print(input)
    input_df = pd.DataFrame.from_dict(input)
    input_df['DtNascimento'] = pd.to_datetime(input_df['DtNascimento'])
    input_df['DtEmissao'] = pd.to_datetime(input_df['DtEmissao']).dt.normalize()
    input_df['Idade'] = ((input_df['DtEmissao'] - input_df['DtNascimento']).dt.days)/365

    df_ceps = pd.read_csv('bases/brasil-ceps.csv',low_memory=False).drop(columns = 'Unnamed: 0')
    input_df = pd.merge(input_df, df_ceps, on='CEP', how='left')

    input_df['cidade_chave'] = input_df['cidade'].str.replace(r'\W', '', regex=True)
    input_df['cidade_chave'] = input_df['cidade_chave'].apply(unidecode)
    input_df['cidade_chave'] = input_df['cidade_chave'].apply(str.upper)

    censo = pd.read_csv('bases/censo10.csv')
    cdestados = pd.read_excel('bases/cdestados.xlsx')

    input_df = pd.merge(input_df,cdestados, left_on='estado',right_on='Estado', how='left')
    input_df['cod_municipio'] = input_df['cidade_chave'] + input_df['Codigo'].astype('string')

    input_df = pd.merge(input_df,censo, on='cod_municipio', how='left').drop(columns=['Município','cod_municipio','Codigo','cidade_chave','Estado','UF','DtNascimento','CEP'])
    input_df['bairro'] = input_df['bairro'] + ' ' + input_df['cidade']
    input_df['mesemissao'] = pd.DatetimeIndex(input_df['DtEmissao']).month
    input_df.drop(columns='DtEmissao', inplace=True)
    return input_df

def previsao(X):
    X = column_trans.transform(X)
    proba = rfc.predict_proba(X)[0][1]
    return proba

app = Flask('propensao_residencial')
@app.route('/previsao', methods = ['POST'])
def previsao_endpoint():
    dados = request.get_json()
    features = prepara_features(dados)
    pred = previsao(features)
    result = {'propensao_residencial':pred}
    return jsonify (result)

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port = '9696')