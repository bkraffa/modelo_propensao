from src import pre_processamento,enriquecimento_cep,prepara_treino,avalia_modelo
from sklearn.ensemble import RandomForestClassifier
import pickle

if __name__ == "__main__":
    df,df_ceps,df_censo,cdestados = pre_processamento.prepara_dfs()
    df_final = enriquecimento_cep.enriquece_cep(df,df_ceps,cdestados,df_censo)
    X_train, X_test, y_train, y_test = prepara_treino.prepara_treino(df_final)
    rfc = RandomForestClassifier(max_depth=9,n_estimators=50,max_features=5)
    rfc.fit(X_train,y_train)
    with open('objetos/modelo_rfc.b', 'wb') as f:
        pickle.dump(rfc, f, -1)
    rfc_predict = rfc.predict(X_test)
    avalia_modelo.avalia_modelo(rfc_predict,X_test,y_test,rfc)


