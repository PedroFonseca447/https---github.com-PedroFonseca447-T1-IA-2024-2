import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier

# Caminhos dos arquivos CSV
train_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTreino.csv'
validation_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetValidacao.csv'
test_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTeste.csv'


def load_data(file_path, sep=','):
    data = pd.read_csv(file_path, sep=sep)
    
  
    print(f"Primeiras linhas de {file_path}:")
    print(data.head())

   
    X = data.iloc[:, :-1].values  
    y = data.iloc[:, -1].values  
    
    return X, y


X_train, y_train = load_data(train_file_path, sep=',')
X_val, y_val = load_data(validation_file_path, sep=',')
X_test, y_test = load_data(test_file_path, sep=',')


mlp = MLPClassifier(hidden_layer_sizes=(5), max_iter=100)
mlp.fit(X_train, y_train)


y_val_pred = mlp.predict(X_val)


val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred, average='weighted')
val_recall = recall_score(y_val, y_val_pred, average='weighted')
val_f1 = f1_score(y_val, y_val_pred, average='weighted')


print("Resultados de Validação (MLP):")
print(f"Acurácia: {val_accuracy}")
print(f"Precisão: {val_precision}")
print(f"Recall: {val_recall}")
print(f"F1-Measure: {val_f1}")


y_test_pred = mlp.predict(X_test)


test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='weighted')
test_recall = recall_score(y_test, y_test_pred, average='weighted')
test_f1 = f1_score(y_test, y_test_pred, average='weighted')


print("Resultados de Teste (MLP):")
print(f"Acurácia: {test_accuracy}")
print(f"Precisão: {test_precision}")
print(f"Recall: {test_recall}")
print(f"F1-Measure: {test_f1}")
