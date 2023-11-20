from src import pre_processamento,enriquecimento_cep,prepara_treino,avalia_modelo
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
import numpy as np

if __name__ == "__main__":
    df,df_ceps,df_censo,cdestados = pre_processamento.prepara_dfs()
    df_final = enriquecimento_cep.enriquece_cep(df,df_ceps,cdestados,df_censo)
    X_train, X_test, y_train, y_test = prepara_treino.prepara_treino(df_final)
    rfc = RandomForestClassifier(max_depth=9,n_estimators=50,max_features=5)
    rfc.fit(X_train,y_train)
    rfc_predict = rfc.predict_proba(X_test)
    prob_compra = [item[1] for item in rfc_predict]
    prob_compra = np.array(prob_compra)
    percentis = np.percentile(prob_compra, [25, 50, 75])

    print("percentil 25:", percentis[0])
    print("percentil 50 (mediana):", percentis[1])
    print("percentil 75:", percentis[2])