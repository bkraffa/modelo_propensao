from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import pickle5 as pickle

def prepara_treino(df):
    y = df.Ramo
    X = df.drop(columns='Ramo')

    numerical_ix = X.select_dtypes(include=['int64', 'float64','int32']).columns
    categorical_ix = X.select_dtypes(include=['object', 'bool']).columns

    column_trans = ColumnTransformer([('cat', OrdinalEncoder(),categorical_ix),
      ('num', MinMaxScaler(feature_range=(-1, 1), ), numerical_ix)],
     remainder='drop')

    column_trans.fit(X)

    with open('objetos/custom_transformer_pickle.b', 'wb') as f:
      pickle.dump(column_trans, f, -1)

    X = column_trans.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    return X_train, X_test, y_train, y_test