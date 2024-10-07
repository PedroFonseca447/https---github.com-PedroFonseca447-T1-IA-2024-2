from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
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


def train_model(game_data):
    X = game_data.iloc[:, :-1].values 
    y = game_data.iloc[:, -1].values   
    
    
    decision_tree = DecisionTreeClassifier(random_state=200)
    decision_tree.fit(X, y)
    return decision_tree


file_path_game = 'C:\\Users\\Windows\\Documents\\IA-t1\\entrega\\coletaDados\\datasets\\DataSetTreino.csv'  # Estados com "X venceu", "O venceu", e "Empate"


game_data = pd.read_csv(file_path_game, sep=',')


decision_tree = train_model(game_data)

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

     
        prediction = decision_tree.predict(encoded_board)[0]

        
        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
