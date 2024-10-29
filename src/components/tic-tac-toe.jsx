import React, { useRef, useState } from "react";
import "../components/TicTacToe.css";
import circle_icon from "../images/circle.png";
import cross_icon from "../images/cross.png";

const TicTacToe = () => {
    const [data, setData] = useState(Array(9).fill(null));
    const [count, setCount] = useState(0);
    const [winner, setWinner] = useState(null);
    const [winnerMessage, setWinnerMessage] = useState("Jogo da Velha");
    const [statusMessage, setStatusMessage] = useState("");
    const containerRef = useRef(null);

    const winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Colunas
        [0, 4, 8], [2, 4, 6]             // Diagonais
    ];

    const toggle = (e, index) => {
        if (data[index] || winner) return;

        const newData = [...data];
        newData[index] = "X";
        setData(newData);
        setCount(count + 1);

        if (checkWinner(newData)) return;

        if (count < 8) {
            const bestMove = getBestMove(newData);
            newData[bestMove] = "O";
            setData(newData);
            setCount(count + 1);
            checkWinner(newData);
        }
    };

    const checkWinner = (squares) => {
        for (let [a, b, c] of winningCombinations) {
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                setWinner(squares[a]);
                setWinnerMessage(`Jogador ${squares[a]} ganhou!`);
                setStatusMessage(`Parabéns! Jogador ${squares[a]} é o vencedor!`);
                return true;
            }
        }

        if (squares.every(square => square !== null)) {
            setWinnerMessage("Empate!");
            setStatusMessage("O jogo terminou em empate!");
            setWinner("Empate");
            return true;
        }
        return false;
    };

    const getBestMove = (board) => {
        let bestScore = Infinity;
        let move;

        for (let i = 0; i < board.length; i++) {
            if (!board[i]) {
                board[i] = "O";
                let score = minimax(board, 0, true); // True aqui porque agora é a vez do "X" maximizar
                board[i] = null;
                if (score < bestScore) {
                    bestScore = score;
                    move = i;
                }
            }
        }
        return move;
    };

    const minimax = (board, depth, isMaximizing) => {
        const result = evaluateBoard(board);
        if (result !== null) return result;

        if (isMaximizing) {
            let bestScore = -Infinity;
            for (let i = 0; i < board.length; i++) {
                if (!board[i]) {
                    board[i] = "X";
                    let score = minimax(board, depth + 1, false);
                    board[i] = null;
                    bestScore = Math.max(score, bestScore);
                }
            }
            return bestScore;
        } else {
            let bestScore = Infinity;
            for (let i = 0; i < board.length; i++) {
                if (!board[i]) {
                    board[i] = "O";
                    let score = minimax(board, depth + 1, true);
                    board[i] = null;
                    bestScore = Math.min(score, bestScore);
                }
            }
            return bestScore;
        }
    };

    const evaluateBoard = (board) => {
        for (let [a, b, c] of winningCombinations) {
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return board[a] === "O" ? -10 : 10;
            }
        }
        return board.every(square => square !== null) ? 0 : null;
    };

    const reset = () => {
        setData(Array(9).fill(null));
        setWinnerMessage("Jogo da Velha");
        setCount(0);
        setWinner(null);
        setStatusMessage("");
    };

    return (
        <div className='container' ref={containerRef}>
            <h1 className='title'>
                {winnerMessage}
            </h1>
            <p className='status'>
                {statusMessage}
            </p>
            <div className='board'>
                {data.map((value, index) => (
                    <div
                        key={index}
                        className='boxes'
                        onClick={(e) => toggle(e, index)}
                    >
                        {value && <img src={value === "X" ? cross_icon : circle_icon} alt={value} />}
                    </div>
                ))}
            </div>
            <button className='reset' onClick={reset}>
                Reset
            </button>
        </div>
    );
};

export default TicTacToe;
