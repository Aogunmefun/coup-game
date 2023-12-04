import React, { useState, 
  createContext, 
  useEffect
} from 'react';
import './app.css';
import { HashRouter, 
  Routes, 
  Route,

} from 'react-router-dom';
import axios from 'axios';


import Navbar from './components/navbar/navbar';
import Home from './pages/home/home';
import Instructions from './pages/instructions/instructions';
import Play from './pages/play/play';

export const Context = createContext()


function App() {

  const [game, setGame] = useState({})
  const [choices, setChoices] = useState({
    action:{
      
    },
    counterAction:{

    },
    challenge: {

    }
  })
  const [targetPlayer, setTargetPlayer] = useState(game.activePlayers?.filter((el)=>el!==game.turn)[0])
  const [moves, setMoves] = useState([])
  const [activePlayers, setActivePlayers] = useState([])
  const [botTime, setBotTime] = useState(false)

  useEffect(()=>{
    setTargetPlayer(game.activePlayers?.filter((el)=>el!==game.turn)[0])
    setActivePlayers(game.activePlayers?.filter((el)=>el!==game.turn))
  },[game])

  const createGame = ()=>{
      axios({
          url:"http://localhost:5000/createGame",
          method:"POST",
          headers:{"Content-Type":"application/json"},
          data:{
              cardCopies:3,
              startingCoins:50,
              numPlayers:4
          }
      }).then((res)=>{
          console.log(res.data)
          setGame(res.data)
          setMoves([])
          setChoices({
            action:{
              
            },
            counterAction:{
        
            },
            challenge: {
        
            }
          })
          setTargetPlayer(game.activePlayers?.filter((el)=>el!==game.turn)[0])
          setActivePlayers(game.activePlayers?.filter((el)=>el!==game.turn))
          setBotTime(true)
      }).catch((e)=>{
          console.log(e)
          alert(e.message)
      })
  }

  const selectAction = (action)=>{
    console.log("target Player", targetPlayer)
    let temp = choices
    temp.action = {
      player:game.turn,
      name:action.name,
      target:targetPlayer
    }
    setChoices({...temp})
    sendAction(action)
    setMoves([...moves, `Player ${game.turn+1} chose ${action.name}`])
  }

  const sendAction = (action)=>{
    console.log("sent",{
      action:action,
          player:game.turn,
    })
    axios({
      url:"http://localhost:5000/selectAction",
      method:"POST",
      headers:{"Content-Type":"application/json"},
      data:{
          action:action,
          player:game.turn,
      }
    }).then((res)=>{
      setGame(res.data)
      setBotTime(true)
      console.log("received Action ack")
    }).catch((e)=>{
      console.log(e)
      alert(e.message)
    })
  }

  const challenge = (action)=>{
    
    let temp = choices
      temp.challenge = {
        player:2,
        target:action==="action"?temp.action.player:temp.action.target,
    }
    setMoves([...moves, `Player 3 chose to challenge Player ${action==="action"?temp.action.player+1:temp.action.target+1}'s 
    ${action==="action"?temp.action.name:temp.counterAction.name}
    `])
    setChoices({...temp})
    setGame({
      ...game,
      phase:"Resolution"
    })
  }

  const counterAction = (name)=>{
    
    let temp = choices
    temp.counterAction = {
      player:choices.action.target,
      name:name
    }
    // console.log("counter", temp.counterAction)
    setMoves([...moves, `Player ${temp.counterAction.player+1} chose to Counteract ${temp.action.name} with ${name}`])
    setChoices({...temp})
    setGame({
      ...game,
      phase:"Challenge"
    })
  }

  const resolveRound = ()=>{
    console.log("choices", choices)
    axios({
      url:"http://localhost:5000/processRound",
      method:"POST",
      headers:{"Content-Type":"application/json"},
      data:choices
    }).then((res)=>{
      setGame(res.data)
      setChoices(
        {
          action:{
      
          },
          counterAction:{
      
          },
          challenge: {
      
          }
        }
      )
      setBotTime(true)
      console.log("rec", res.data)
    }).catch((e)=>{
      console.log(e)
      alert(e.message)
    })
  }

  return (
    <div className="app">
      
      <HashRouter>
        {/* <Navbar /> */}
        <Context.Provider value={{
          game:game,
          setGame:setGame,
          createGame:createGame,
          choices:choices,
          challenge:challenge,
          selectAction:selectAction,
          resolveRound:resolveRound,
          targetPlayer:targetPlayer,
          setTargetPlayer:setTargetPlayer,
          counterAction:counterAction,
          moves:moves,
          setMoves:setMoves,
          activePlayers:activePlayers,
          botTime:botTime,
          setBotTime:setBotTime
        }}>
          <Routes>
            <Route path='/' element={<Play />} />
            <Route path='/home' element={<Home />} />
            <Route path='/instructions' element={<Instructions />} />
            <Route path='/play' element={<Play />} />
          </Routes>
        </Context.Provider>
        
      </HashRouter>
    </div>
      
  
  );
}

export default App;
