from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para codificar o tabuleiro em formato numérico (1 para X, -1 para O, 0 para vazio)
def encode_board(board):
    encoded = []
    for cell in board:
        if cell == 'X':
            encoded.append(1)
        elif cell == 'O':
            encoded.append(-1)
        else:
            encoded.append(0)  # Trata null ou vazio como 0
    return encoded

# Treinar o modelo KNN com o dataset fornecido
def train_model(game_data):
    X = game_data.iloc[:, :-1].values  # As primeiras colunas são os estados do tabuleiro
    y = game_data.iloc[:, -1].values   # A última coluna é o resultado
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    return knn

# Ajuste no caminho dos arquivos de treinamento
file_path_game = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\dataSetFinal.csv'  # Estados com "X venceu", "O venceu", "Empate" e "Tem jogo"

# Ler o arquivo CSV
game_data = pd.read_csv(file_path_game, sep=';')

# Treinar o modelo com os dados fornecidos
knn = train_model(game_data)

@app.route('/check_winner', methods=['POST'])
def predict_winner():
    data = request.json
    board = data.get('board', [])

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    # Codificar o tabuleiro para o modelo
    encoded_board = np.array([encode_board(board)])
    
    # Fazer a previsão com o KNN
    prediction = knn.predict(encoded_board)[0]

    # Interpretar a previsão
    if prediction == 1:
        result = 'X venceu'
    elif prediction == -1:
        result = 'O venceu'
    elif prediction == 0:
        result = 'Empate'
    elif prediction == 2:
        result = 'Tem jogo'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
