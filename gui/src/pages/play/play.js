import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import "./play.css"
import { Context } from "../../app";

import Board from "../../components/board/board";
import ChatWindow from "../../components/chatWindow/chatWindow";
function Play() {
    
    let app = useContext(Context)

    useEffect(()=>{
        
    },[])


    return(
        <div className="play">
            
            {
                !app.game.players?
                <button onClick={()=>app.createGame()} className="btn--play">Generate New Game</button>
                :<>
                    <button onClick={()=>app.createGame()} className="btn--generate-game"> <i className="material-icons">refresh</i>Generate New Game</button>
                    <ChatWindow 
                        messages={app.moves}
                        windowSize={"200px"}
                    />
                    <Board />
                </>
            }
            
        </div>
    )
}

export default Play