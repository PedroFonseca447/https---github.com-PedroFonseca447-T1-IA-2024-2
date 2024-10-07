import React, { useRef, useState } from "react";
import axios from "axios"; 
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

    const toggle = (e, index) => {
       
        if (data[index] || winner) return;

        const newData = [...data];

        if (count % 2 === 0) {
            newData[index] = "X";
            containerRef.current.style.cursor = `url(${circle_icon}), auto`;
        } else {
            newData[index] = "O";
            containerRef.current.style.cursor = `url(${cross_icon}), auto`;
        }

        setData(newData);
        setCount(count + 1);

    
        if (count >= 4) {
            handlePlay(newData);
        }
    };


    async function checkWinner(squares) {
        try {
            console.log("Enviando tabuleiro para o backend:", squares);  
            const response = await axios.post('http://localhost:5000/check_winner', {
                board: squares,
            });
            console.log("Resposta do backend: ", response.data); 
            setWinner(response.data.winner); 

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
      
        const numberOfMoves = newData.filter(square => square !== null).length;
        
        if (numberOfMoves >= 5) {
            checkWinner(newData);
        }
        
        if (numberOfMoves === 9 && !winner) {
            setWinnerMessage("Empate!");
            setStatusMessage("O jogo terminou em empate!");
            setWinner("Empate");
        }
    };

    const reset = () => {
        setData(Array(9).fill(null)); 
        setWinnerMessage("Jogo da Velha");
        setCount(0);
        containerRef.current.style.cursor = `url(${cross_icon}), auto`; 
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
