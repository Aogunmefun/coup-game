import React, { useContext, useState, useEffect } from 'react';
import PlayerUI from '../playerUI/playerUI';
import './board.css';
import { Context } from '../../app';

import DropdownMenu from '../dropDownMenu/dropDownMenu';
import NumberPicker from '../numberPicker/numberPicker';

const Board = () => {

    
    let game = useContext(Context)
    // const [number, setNumber] = useState(game.game.activePlayers.filter((el)=>el!==game.game.turn)[0])
    // console.log("number", number)

    // useEffect(()=>{
    //     game.setTargetPlayer(number);
    // },[])

    const handleNumberChange = (num)=>{
        game.setTargetPlayer(num-1);
    }
  return (
    <div className="game-board">
        {
            game.game.phase==="Challenge"?
                <div className="board-buttons">
                    {
                        game.choices.action.name?<button onClick={()=>game.challenge("action")}>Challenge Action</button>:"" 
                    }
                    {
                        game.choices.counterAction.name?<button onClick={()=>game.challenge("cact")}>Challenge Counter Action</button>:""
                    }
                    {
                        <button onClick={()=>game.setGame({...game.game, phase:"Resolution"})}>Don't Challenge</button>
                    }
                </div>
            :""
        }
        {
            game.game.phase==="Counter-Action"?
            <div className="board-buttons">
                <button onClick={()=>game.setGame({...game.game, phase:"Challenge"})}>Don't Counter-Action</button>
            </div>
            :""
        }
        {
            game.game.phase==="Resolution"?
            <button className='btn--resolve' onClick={()=>game.resolveRound()}>Resolve Round</button>
            :""
        }
        
        
        <div className="game-info">
            <p>Round: {game.game.round}</p>
            <p>Turn: Player {game.game.turn+1} </p>
            <p>Phase: {game.game.phase}</p>
        </div>
        <div className="board-menu">
                <DropdownMenu
                    choices={game.game.actions}
                />
                <NumberPicker 
                    
                />
                
            
        </div>
        
        <div className="players">
            {
                game.game.players?.map((player,index)=>{
                    return(
                        <div className="player">
                            <PlayerUI 
                                inventory={player} 
                                side={index%2!==0?index===1?"right":"left":""} 
                                ai={index!==2?true:false} 
                                playerIndex={index}
                            />
                        </div>
                    )
                })
            }
        </div>
        
        <div className="chest">
            <div className="bank">
                {game.game.bank}
            </div>
            <div className="deck">
                <p>Deck</p>
                
                <p>{game.game.cards.length}</p>
            </div>
        </div>
        
    </div>
    );
};

export default Board;