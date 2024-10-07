from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

# Caminhos dos arquivos CSV
train_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTreino.csv'
validation_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetValidacao.csv'
test_file_path = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\dataSetTeste.csv'

# Função para carregar os dados de um CSV sem conversão de tipo
def load_data(file_path, sep=','):
    # Ler o CSV com o separador especificado
    data = pd.read_csv(file_path, sep=sep)
    
    # Exibe as primeiras linhas do dataset para confirmar a leitura
    print(f"Primeiras linhas de {file_path}:")
    print(data.head())

    # Separar as colunas de features (X) e rótulos (y)
    X = data.iloc[:, :-1].values  # Features (tabuleiro)
    y = data.iloc[:, -1].values   # Rótulos (resultado do jogo)
    
    return X, y

# Carregar os dados de treino e validação
X_train, y_train = load_data(train_file_path, sep=',')
X_val, y_val = load_data(validation_file_path, sep=',')
X_test, y_test = load_data(test_file_path, sep= ',')

# Treinar o modelo KNN com os dados de treino
knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train, y_train)

# Validar o modelo com os dados de validação
y_val_pred = knn.predict(X_val)

# Calcular métricas
val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred, average='weighted')
val_recall = recall_score(y_val, y_val_pred, average='weighted')
val_f1 = f1_score(y_val, y_val_pred, average='weighted')

# Exibir resultados
print("Resultados de Validação:")
print(f"Acurácia: {val_accuracy}")
print(f"Precisão: {val_precision}")
print(f"Recall: {val_recall}")
print(f"F1-Measure: {val_f1}")



knn.fit(X_test, y_test)

# Validar o modelo com os dados de validação
y_test_pred = knn.predict(X_test)

# Calcular métricas
val_accuracy = accuracy_score(y_test, y_test_pred)
val_precision = precision_score(y_test, y_test_pred, average='weighted')
val_recall = recall_score(y_test, y_test_pred, average='weighted')
val_f1 = f1_score(y_test, y_test_pred, average='weighted')

# Exibir resultados
print("Resultados de teste:")
print(f"Acurácia: {val_accuracy}")
print(f"Precisão: {val_precision}")
print(f"Recall: {val_recall}")
print(f"F1-Measure: {val_f1}")