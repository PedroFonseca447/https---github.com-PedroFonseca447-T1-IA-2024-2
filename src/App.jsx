import { useState } from 'react';
import axios from 'axios'; // Para fazer requisições HTTP

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board({ xIsNext, squares, onPlay }) {
  function handleClick(i) {
    if (squares[i] || squares.every(Boolean)) {
      return; // Impede que uma célula já preenchida ou tabuleiro completo seja clicada
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    onPlay(nextSquares);
  }

  return (
    <>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const [winner, setWinner] = useState(null); // Estado para o vencedor
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];

  // Função para verificar o vencedor no backend
  async function checkWinner(squares) {
    try {
      console.log("Enviando tabuleiro para o backend:", squares);  // Verificar o estado do tabuleiro enviado
      const response = await axios.post('http://localhost:5000/check_winner', {
        board: squares,
      });
      console.log("Resposta do backend: ", response.data); // Verificar a resposta do backend
      setWinner(response.data.winner); // Definir o vencedor com base na resposta do backend
    } catch (error) {
      console.error('Erro ao verificar o vencedor:', error);
    }
  }

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);

    // Contar o número de jogadas (não vazios)
    const numberOfMoves = nextSquares.filter(square => square !== null).length;

    // Só verificar o vencedor se houver pelo menos 5 jogadas
    if (numberOfMoves >= 5) {
      checkWinner(nextSquares);
    }
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
    setWinner(null); // Redefine o vencedor ao voltar para um movimento anterior
  }

  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = 'Go to move #' + move;
    } else {
      description = 'Go to game start';
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });

  let status;
if (winner === 'Empate') {
  status = 'Empate!';
} else if (winner === 'Tem jogo') {
  status = 'O jogo ainda está em andamento!';
} else if (winner) {
  status = 'Winner: ' + winner;
} 

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <div>{status}</div>
        <ol>{moves}</ol>
      </div>
    </div>
  );
}
