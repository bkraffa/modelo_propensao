import pandas as pd
from unidecode import unidecode

def enriquece_cep(df,df_ceps,cdestados,df_censo):
    df_ceps.CEP = df_ceps.CEP.astype('int64')
    df_ceps.sort_values(by=['CEP'], inplace=True)
    df_ceps.reset_index(inplace=True,drop=True)

    df = pd.merge(df, df_ceps, on='CEP', how='left')
    df.dropna(subset=['bairro'], inplace=True)
    df.drop(columns=['UN','CdCliente','DtNascimento','EstadoCivil','CEP','Cidade','Bairro','Estado'], inplace=True)

    df['cidade_chave'] = df['cidade'].str.replace(r'\W', '', regex=True)
    df['cidade_chave'] = df['cidade_chave'].apply(unidecode)
    df['cidade_chave'] = df['cidade_chave'].apply(str.upper)

    df = pd.merge(df,cdestados, left_on='estado',right_on='Estado', how='left')
    df['cod_municipio'] = df['cidade_chave'] + df['Codigo'].astype('string')

    df_final = pd.merge(df,df_censo, on='cod_municipio', how='left').drop(columns=['Município','cod_municipio','Codigo','cidade_chave','Estado','UF'])
    df_final['bairro'] = df_final['bairro'] + ' ' + df_final['cidade']
    df_final['mesemissao'] = pd.DatetimeIndex(df['DtEmissao']).month
    df_final.drop(columns='DtEmissao', inplace=True)

    df_final.loc[df_final['Ramo'] != 'Residencial','Ramo'] = 0
    df_final.loc[df_final['Ramo'] == 'Residencial','Ramo'] = 1
    df_final.Ramo = df_final.Ramo.astype('int64')
    df_final = df_final.dropna()

    return df_final
