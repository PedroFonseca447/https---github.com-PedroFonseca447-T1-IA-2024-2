import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score

# Função para validar o modelo com métricas de acurácia e precisão
def validate_model(model, X, y, dataset_name):
    # Fazer as previsões no conjunto (validação ou teste)
    y_pred = model.predict(X)
    
    # Calcular a acurácia
    accuracy = accuracy_score(y, y_pred)
    
    # Calcular a precisão ponderada (considerando o desbalanceamento de classes)
    precision = precision_score(y, y_pred, average='weighted', zero_division=0)
    
    # Exibir as métricas
    print(f"Resultados para {dataset_name}:")
    print(f"Acurácia: {accuracy:.2f}")
    print(f"Precisão: {precision:.2f}\n")
    
    return accuracy, precision

# Carregar os dados de treino para treinar o modelo
X_train = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Train').drop(columns=['result']).values
y_train = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Train')['result'].values

# Definir e treinar o modelo KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Preparar os dados de validação
X_val = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Validation').drop(columns=['result']).values
y_val = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Validation')['result'].values

# Avaliar o modelo no conjunto de validação
val_accuracy, val_precision = validate_model(knn, X_val, y_val, "Validação")

# Preparar os dados de teste
X_test = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Test').drop(columns=['result']).values
y_test = pd.read_excel('coletaDados/prepared_tic_tac_toe_dataset.xlsx', sheet_name='Test')['result'].values

# Avaliar o modelo no conjunto de teste
test_accuracy, test_precision = validate_model(knn, X_test, y_test, "Teste")

# Comparação de resultados
print("Comparação de Resultados:")
print(f"Acurácia - Validação: {val_accuracy:.2f} vs. Teste: {test_accuracy:.2f}")
print(f"Precisão - Validação: {val_precision:.2f} vs. Teste: {test_precision:.2f}")


