import React, { useContext } from 'react';
import './numberPicker.css';

import { Context } from '../../app';

const NumberPicker = () => {

    const app = useContext(Context)

  const handleNumberChange = (event) => {
    const selectedNumber = parseInt(event.target.value, 10);
    app.setTargetPlayer(selectedNumber);
  };

  return (
    <div className="num-picker-container">
        <p>Target Player</p>
        <select className="number-picker" onChange={handleNumberChange}>
        
            {app.game.activePlayers?.map((number, index) => (
            <option defaultValue={index===0} key={number} value={number}>
                {number+1}
            </option>
            ))}
        </select>
    </div>
    
  );
};

export default NumberPicker;