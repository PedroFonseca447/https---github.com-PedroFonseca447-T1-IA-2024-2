from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

# Caminhos dos arquivos CSV
train_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTreino.csv'
validation_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetValidacao.csv'
test_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTeste.csv'

# Função para carregar os dados de um CSV
def load_data(file_path, sep=','):
  
    data = pd.read_csv(file_path, sep=sep)
    
   
    print(f"Primeiras linhas de {file_path}:")
    print(data.head())

   
    X = data.iloc[:, :-1].values  
    y = data.iloc[:, -1].values   
    
    return X, y

# Carregar os dados de treino, validação e teste
X_train, y_train = load_data(train_file_path, sep=',')
X_val, y_val = load_data(validation_file_path, sep=',')
X_test, y_test = load_data(test_file_path, sep=',')

# Treinar o modelo de Árvore de Decisão com os dados de treino
decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)

# Validar o modelo com os dados de validação
y_val_pred = decision_tree.predict(X_val)

# Calcular métricas nos dados de validação
val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred, average='weighted')
val_recall = recall_score(y_val, y_val_pred, average='weighted')
val_f1 = f1_score(y_val, y_val_pred, average='weighted')

# Exibir resultados da validação
print("Resultados de Validação (Árvore de Decisão):")
print(f"Acurácia: {val_accuracy}")
print(f"Precisão: {val_precision}")
print(f"Recall: {val_recall}")
print(f"F1-Measure: {val_f1}")

# Avaliar o modelo com os dados de teste
y_test_pred = decision_tree.predict(X_test)

# Calcular métricas nos dados de teste
test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='weighted')
test_recall = recall_score(y_test, y_test_pred, average='weighted')
test_f1 = f1_score(y_test, y_test_pred, average='weighted')

# Exibir resultados do teste
print("Resultados de Teste (Árvore de Decisão):")
print(f"Acurácia: {test_accuracy}")
print(f"Precisão: {test_precision}")
print(f"Recall: {test_recall}")
print(f"F1-Measure: {test_f1}")