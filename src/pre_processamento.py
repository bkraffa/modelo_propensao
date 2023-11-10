import pandas as pd
import os
from unidecode import unidecode

def prepara_dfs():
    df = pd.read_csv('bases/basefull.csv',sep=';' ,header=None)
    df_ceps = pd.read_csv('bases/brasil-ceps.csv',sep=',').drop(columns = 'Unnamed: 0')
    cdestados = pd.read_excel('bases/cdestados.xlsx')
    df_censo = pd.read_csv('bases/censo10.csv')
    
    df.columns = ['DtEmissao','UN','Ramo','CdCliente','DtNascimento','Sexo','EstadoCivil','CEP','Cidade','Bairro','Estado']
    df.loc[df['Estado'] == 'Acre', 'Estado'] = 'AC'
    df.loc[df['Estado'] == 'Alagoas', 'Estado'] = 'AL'
    df.loc[df['Estado'] == 'Amapá', 'Estado'] = 'AP'
    df.loc[df['Estado'] == 'Amazonas', 'Estado'] = 'AM'
    df.loc[df['Estado'] == 'Bahia', 'Estado'] = 'BA'
    df.loc[df['Estado'] == 'Ceará', 'Estado'] = 'CE'
    df.loc[df['Estado'] == 'Bahia', 'Estado'] = 'BA'
    df.loc[df['Estado'] == 'Distrito Federal', 'Estado'] = 'DF'
    df.loc[df['Estado'] == 'Espírito Santo', 'Estado'] = 'ES'
    df.loc[df['Estado'] == 'Goiás', 'Estado'] = 'GO'
    df.loc[df['Estado'] == 'Maranhão', 'Estado'] = 'MA'
    df.loc[df['Estado'] == 'Mato Grosso', 'Estado'] = 'MT'
    df.loc[df['Estado'] == 'Mato Grosso do Sul', 'Estado'] = 'MS'
    df.loc[df['Estado'] == 'Minas Gerais', 'Estado'] = 'MG'
    df.loc[df['Estado'] == 'Paraná', 'Estado'] = 'PR'
    df.loc[df['Estado'] == 'Paraíba', 'Estado'] = 'PB'
    df.loc[df['Estado'] == 'Pará', 'Estado'] = 'PA'
    df.loc[df['Estado'] == 'Pernambuco', 'Estado'] = 'PE'
    df.loc[df['Estado'] == 'Piauí', 'Estado'] = 'PI'
    df.loc[df['Estado'] == 'Rio Grande do Norte', 'Estado'] = 'RN'
    df.loc[df['Estado'] == 'Rio Grande do Sul', 'Estado'] = 'RS'
    df.loc[df['Estado'] == 'Rio de Janeiro', 'Estado'] = 'RJ'
    df.loc[df['Estado'] == 'Rondônia', 'Estado'] = 'RO'
    df.loc[df['Estado'] == 'Roraima', 'Estado'] = 'RR'
    df.loc[df['Estado'] == 'Santa Catarina', 'Estado'] = 'SC'
    df.loc[df['Estado'] == 'Sergipe', 'Estado'] = 'SE'
    df.loc[df['Estado'] == 'São Paulo', 'Estado'] = 'SP'
    df.loc[df['Estado'] == 'Tocantins', 'Estado'] = 'TO'
    df.loc[df['Estado'] == 'Roraima', 'Estado'] = 'RR'
    df.loc[df['Estado'] == 'Santa Catarina', 'Estado'] = 'SC'
    df.loc[df['Estado'] == 'Sergipe', 'Estado'] = 'SE'
    df.loc[df['Estado'] == 'São Paulo', 'Estado'] = 'SP'
    df.loc[df['Estado'] == 'Tocantins', 'Estado'] = 'TO'
    df = df.loc[df['Estado'] != '00']
    df = df.loc[df['Estado'] != '06']
    df = df.loc[df['Estado'] != '10']
    df = df.loc[df['Estado'] != '15']
    df = df.loc[df['Estado'] != '20']
    df = df.loc[df['Estado'] != '5']
    df = df.loc[df['Estado'] != '71']
    df = df.loc[df['Estado'] != '97']
    df.Estado = df.Estado.astype('str')
    df['Estado'] = df['Estado'].apply(lambda x: x.upper())

    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    df = df[df['Estado'].isin(estados)]

    df['Cidade'] = df['Cidade'].apply(lambda x: x.upper())
    df['Cidade'] = df['Cidade'].str.strip()
    df['Cidade'] = df['Cidade'].apply(unidecode)
    df['Cidade'] = df['Cidade'].str.replace(r'\W', '', regex=True)

    df = df.loc[df['DtNascimento'] != '0001-01-03']
    df = df.loc[df['DtNascimento'] != '0001-01-01']
    df = df.loc[df['DtNascimento'] != '0198-01-07']
    df = df.loc[df['DtNascimento'] != '1378-10-31']
    df = df.loc[df['DtNascimento'] != '1662-08-08']
    df = df.loc[df['DtNascimento'] != '0708-06-28']
    df['DtNascimento'] = pd.to_datetime(df['DtNascimento'])
    df = df[(df['DtNascimento'].dt.year > 1920)]
    df = df[(df['DtNascimento'].dt.year < 2001)]
    df['DtEmissao'] = pd.to_datetime(df['DtEmissao']).dt.normalize()
    df['Idade'] = ((df['DtEmissao'] - df['DtNascimento']).dt.days)/365
    df.CdCliente = df.CdCliente.astype('str')
    df['chave'] = df.CdCliente + df.Ramo
    df = df.sort_values(by='DtEmissao')
    df = df.drop_duplicates(subset='chave', keep='first').drop(columns='chave').reset_index(drop=True)
    df['CEP'] = pd.to_numeric(df['CEP'], errors='coerce')
    df = df[pd.notna(df['CEP'])]
    df.CEP = df.CEP.astype('int64')
    df = df.reset_index(drop=True)
    df = df.loc[df['CEP'] > 1000001]
    df = df.loc[df['CEP'] < 99999999]

    return df,df_ceps,df_censo,cdestados