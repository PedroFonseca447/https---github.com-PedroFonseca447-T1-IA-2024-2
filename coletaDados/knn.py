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
def train_model(game_data, ongoing_data):
    # Combinar os datasets de jogo terminado e jogo em andamento
    combined_data = pd.concat([game_data, ongoing_data], ignore_index=True)
    
    X = combined_data.iloc[:, :-1].values  # As primeiras colunas são os estados do tabuleiro
    y = combined_data.iloc[:, -1].values   # A última coluna é o resultado
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    return knn

file_path_game = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\dataSetTreino.csv'  # Estados com "X venceu", "O venceu", e "Empate"
file_path_ongoing = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\dataSetAdicional.csv'  # Estados com "Tem jogo"

# Ler os arquivos CSV
game_data = pd.read_csv(file_path_game, sep=',')
ongoing_data = pd.read_csv(file_path_ongoing, sep=',')

# Treinar o modelo com os dois datasets
knn = train_model(game_data, ongoing_data)

@app.route('/check_winner', methods=['POST'])
def predict_winner():
    data = request.json
    board = data.get('board', [])

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    # Primeiro, verificamos se ainda há espaços vazios, ou seja, o jogo está em andamento
    if '' in board:
        result = 'Em andamento'
    else:
        # Se o tabuleiro estiver completo, codificar o tabuleiro para o modelo
        encoded_board = np.array([encode_board(board)])
        
        # Fazer a previsão com o KNN
        prediction = knn.predict(encoded_board)[0]

        # Interpretar a previsão
        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
