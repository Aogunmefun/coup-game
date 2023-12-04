import React, { useState, useContext, useEffect } from 'react';
import './dropDownMenu.css';
import { Context } from '../../app';
import useFlashMessage from '../../hooks/useFlashMessage/useFlashMessage';

const DropdownMenu = ({ choices }) => {
    const [isExpanded, setExpanded] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);

    const app = useContext(Context)

    useEffect(()=>{
        if (((app.game.turn !== 2)||((app.game.phase==="Counter-Action")&&(app.choices.action.target!==2)))&&(app.activePlayers)) {
            // if (app.game.phase!=="Challenge"&&app.game.phase!=="Resolution") {
            //     app.setMoves([...app.moves, `Player ${app.game.phase==="Action"?app.game.turn+1:app.choices.action.target+1} is Thinking... `])
            // }
            console.log("botTime??", app.botTime)
            if (((app.game.phase!=="Resolution")||(app.game.phase!=="Challenge"))&&app.botTime) {
                
                if (((app.game.phase==="Counter-Action")&&(app.game.actions.length>0))||(app.game.phase==="Action")) {
                    
                        
                    setTimeout(() => {
                        console.log("Really Bot Time!!")
                        app.setBotTime(false)
                        let aiChoice = Math.floor(Math.random() * (app.game.actions.length-1))
                        let randomTarget = Math.floor(Math.random() * (app.activePlayers.length-1))
                        // console.log("aiChoice", aiChoice, Math.floor(Math.random()*app.game.actions.length), Math.random(),app.game.actions.length)
                        if (app.game.phase === "Action") {
                            app.setTargetPlayer(randomTarget)
                            app.selectAction(choices[aiChoice])
                            
                        }
                        else if (app.game.phase === "Counter-Action") {
                            let counterActionOrNot = Math.random()
                            if ((counterActionOrNot>0.5)&&app.game.actions.length>0) {
                                app.counterAction(choices[aiChoice])
                            }
                            else {
                                app.setGame({...app.game, phase:"Challenge"})
                            }
                        }
                    }, 1000);
                }
            }
            
            
            
        }
    },[app.activePlayers,app.game.phase,app.botTime])
  
    

    const handleMouseEnter = () => {
      setExpanded(true);
    };
  
    const handleMouseLeave = () => {
      setExpanded(false);
    };
  
    const handleSelect = (option) => {
      setSelectedOption(app.game.phase === "Counter-Action"?option:option.name);
      setExpanded(false);
      let player = app.game.phase==="Action"?app.game.turn+1:4
      if (app.game.phase === "Counter-Action") {
        console.log("yup", app.choices)
        player = app.choices.action.target + 1
        app.counterAction(option)
      }
      else {
        app.selectAction(option)
      }
      
    };
  
    return (
      <div
        className={`hover-dropdown-menu ${isExpanded ? 'expanded' : ''}`}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <div className="toggle">
          {selectedOption ? selectedOption : 'Actions/Counter-Actions'}
        </div>
        {isExpanded && (
          <ul className="options">
            {choices?.map((option, index) => (
            
              <li key={index} onClick={() => handleSelect(option)}>
                {app.game.phase === "Counter-Action"?option:option.name}
              </li>
            ))}
          </ul>
        )}
      </div>
    );
};

export default DropdownMenu;