import React, { useState } from 'react';
import './playerUI.css';

const PlayerUI = ({ inventory, side, ai, playerIndex }) => {
    const [hoveredCard, setHoveredCard] = useState(null);

    const handleCardHover = (card) => {
        if (!ai) setHoveredCard(card)
    };

    const handleCardLeave = () => {
        setHoveredCard(null);
    };

    const renderCardSlot = (card, index) => {
        const isFaceUp = card.flipped;

        return (
        <div
            key={index}
            className={`card-slot ${isFaceUp ? 'face-up' : 'face-down'} ${side?"side-card-slot":""}`}
            onMouseEnter={() => handleCardHover(card)}
            onMouseLeave={handleCardLeave}
        >
            <p className={`card-info ${side?side==="right"?"right-card-info":"left-card-info":""}`}>
                {card.name} <br /> {isFaceUp ? "Face Up" : "Face Down"}
            </p>
        </div>
        );
    };

    const renderCoinSlot = () => {
        return( 
            <div className={`coin-slot ${side?side==="right"?"right-coin-slot":"left-coin-slot":""}`}>
                <p>Player {playerIndex+1}</p>
                Coins: {inventory.coins}
            </div>
        )
    };

    return (
        <div 
            className={`player-ui ${side?side==="right"?"right-player-ui":"left-player-ui":""}`}
        >
            <div className={`card-slots ${side?"side-card-slots":""}`} >
                {inventory.cards.map(renderCardSlot)}
            </div>
            {renderCoinSlot()}

            {hoveredCard && (
                <div className="hover-popup">
                    <h3>{hoveredCard.name}</h3>
                    <p>{"Actions: "+hoveredCard.actions.join(" ,")}</p>
                    <p>{"Counter-Actions: "+hoveredCard.counterActions}</p>
                </div>
            )}
        </div>
    );
};

export default PlayerUI;