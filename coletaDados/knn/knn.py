from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def encode_board(board):
    encoded = []
    for cell in board:
        if cell == 'X':
            encoded.append(1)
        elif cell == 'O':
            encoded.append(-1)
        else:
            encoded.append(0) 
    return encoded


def check_tie(board):
    return all(cell != '' for cell in board)  


def train_model(game_data):
    X = game_data.iloc[:, :-1].values 
    y = game_data.iloc[:, -1].values 
    
    knn = KNeighborsClassifier(n_neighbors=2)
    knn.fit(X, y)
    return knn


file_path_game = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetTreino.csv'


game_data = pd.read_csv(file_path_game, sep=',')


knn = train_model(game_data)

@app.route('/check_winner', methods=['POST'])
def predict_winner():
    data = request.json
    board = data.get('board', [])

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    if '' in board:
        result = 'Em andamento'
    else:
       
        encoded_board = np.array([encode_board(board)])
       
        prediction = knn.predict(encoded_board)[0]
    
        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            
            if check_tie(board):
                result = 'Empate'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
