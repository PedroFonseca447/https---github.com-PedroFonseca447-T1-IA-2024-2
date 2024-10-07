import React, { useRef, useState } from "react";
import axios from "axios"; // Para fazer requisições HTTP
import "../components/TicTacToe.css";
import circle_icon from "../images/circle.png";
import cross_icon from "../images/cross.png";

const TicTacToe = () => {
    const [data, setData] = useState(Array(9).fill(null)); // Usando state para o tabuleiro
    const [count, setCount] = useState(0);
    const [winner, setWinner] = useState(null); // Estado para o vencedor
    const [winnerMessage, setWinnerMessage] = useState("Jogo da Velha"); // Estado para a mensagem de vencedor
    const [statusMessage, setStatusMessage] = useState(""); // Nova mensagem de status para mostrar quem venceu ou empate
    const containerRef = useRef(null);

    const toggle = (e, index) => {
        // Previne modificar uma célula já preenchida ou se já houver um vencedor
        if (data[index] || winner) return;

        const newData = [...data]; // Cópia do estado atual do tabuleiro

        // Alterna entre X e O com base na contagem
        if (count % 2 === 0) {
            newData[index] = "X";
            containerRef.current.style.cursor = `url(${circle_icon}), auto`;
        } else {
            newData[index] = "O";
            containerRef.current.style.cursor = `url(${cross_icon}), auto`;
        }

        setData(newData);
        setCount(count + 1);

        // Verifica vitória ou empate após a quinta jogada (mínimo necessário para uma vitória ou empate)
        if (count >= 4) {
            handlePlay(newData);
        }
    };

    // Função para enviar o tabuleiro para o backend
    async function checkWinner(squares) {
        try {
            console.log("Enviando tabuleiro para o backend:", squares);  // Verificar o estado do tabuleiro enviado
            const response = await axios.post('http://localhost:5000/check_winner', {
                board: squares,
            });
            console.log("Resposta do backend: ", response.data); // Verificar a resposta do backend
            setWinner(response.data.winner); // Definir o vencedor com base na resposta do backend

            if (response.data.winner === 'Empate') {
                setWinnerMessage("Empate!");
                setStatusMessage("O jogo terminou em empate!");
            } else if (response.data.winner) {
                setWinnerMessage(`Jogador ${response.data.winner === "X" ? "X" : "O"} ganhou!`);
                setStatusMessage(`Parabéns! Jogador ${response.data.winner} é o vencedor!`);
            }
        } catch (error) {
            console.error('Erro ao verificar o vencedor:', error);
        }
    }

    const handlePlay = (newData) => {
        // Contar o número de jogadas (não vazios)
        const numberOfMoves = newData.filter(square => square !== null).length;

        // Só verificar o vencedor se houver pelo menos 5 jogadas
        if (numberOfMoves >= 5) {
            checkWinner(newData);
        }

        // Verifica se o tabuleiro está completo sem vencedor para declarar empate
        if (numberOfMoves === 9 && !winner) {
            setWinnerMessage("Empate!");
            setStatusMessage("O jogo terminou em empate!");
            setWinner("Empate");
        }
    };

    const reset = () => {
        setData(Array(9).fill(null)); // Reinicia o estado do tabuleiro
        setWinnerMessage("Jogo da Velha");
        setCount(0);
        containerRef.current.style.cursor = `url(${cross_icon}), auto`; // Reseta o cursor
        setWinner(null); // Reiniciar o estado do vencedor
        setStatusMessage(""); // Reinicia a mensagem de status
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
