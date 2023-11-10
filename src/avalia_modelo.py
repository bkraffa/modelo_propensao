import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score,precision_score,recall_score,f1_score,confusion_matrix

def avalia_modelo(rfc_predict,X_test,y_test,rfc):
    erros = (rfc_predict != y_test).sum()
    print("Resultados do Random Forest Classifier")
    acc= accuracy_score(y_test,rfc_predict)
    print("A acurácia é:  {}".format(acc))
    prec= precision_score(y_test,rfc_predict)
    print("A precisão do modelo é: {}".format(prec))
    rec= recall_score(y_test,rfc_predict)
    print("O recall é: {}".format(rec))
    f1= f1_score(y_test,rfc_predict)
    print("F1 Score é: {}".format(f1))

    #matriz de confusão
    LABELS = ['Não Residencial', 'Residencial']
    conf_matrix = confusion_matrix(y_test, rfc_predict)
    plt.figure(figsize=(6, 6))
    sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d", cmap = 'GnBu');
    plt.title("Matriz de confusão RFC")
    plt.ylabel('Classe Correta')
    plt.xlabel('Classe Prevista')
    plt.show()

    # Métricas
    plt.figure(figsize=(10,6))
    print('{}: {} erros'.format("RFC", erros))
    print(accuracy_score(y_test, rfc_predict))
    print(classification_report(y_test, rfc_predict))

