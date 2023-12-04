# This is where the main logic of the code is contained.
# A flask server is used to process UI requests from the user
# Additionally, for the UI, a simple React front-end will be used in order to make it a bit more visual (and show off a little)

# The game will be run using a player class that represents a player, their possible desicions, and what their current state is (cards, coins, influence etc)
# The number of player classes that are instantiated are simply based on the number of players (AI and human)
# The Cards will be simple ojects that hold the name of the card, the possible actions, and the possible counter-actions


from game import Game # importing the "Game" class which holds most of the game logic
from flask import Flask # Importing flask to host a web server
from flask import request # Importing "request" module from flask to allow us to exract client request parameters
from flask_cors import CORS, cross_origin # Importing "CORS" just in case any errors might pop up during local development
from actions import *
from counterActions import *
import copy

game = "" # Creating a global variable to store the "Game" class object 

# Initializing flask and some parameters (CORS)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Route to create a brand new game
@app.route("/createGame", methods=["POST"])
@cross_origin()
def createGame():
    global game # Making sure that we're talking to the global "game" variable
    # Initializing game and it's parameters
    game = 0
    game = Game(copiesPerCard=request.get_json()["cardCopies"], startingCoins=request.get_json()["startingCoins"], numPlayers=request.get_json()["numPlayers"])
    # Let's return all the information about the newly initialized game so that the UI can render the appropriate elements
    print(p.inventory for p in game.players)
    possibleActions = copy.copy(actions)
    for a in possibleActions:
        if a["name"]=="Assassinate" or a["name"]=="Steal":
            possibleActions.remove(a)
    return {
        "players": [p.inventory for p in game.players],
        "bank":game.bank,
        "actions":possibleActions,
        "player":game.turn,
        "cards":game.cardStack,
        "turn":game.turn,
        "round":game.round,
        "phase":game.phase,
        "activePlayers":game.activePlayers
    }

@app.route("/selectAction", methods=["POST"])
@cross_origin()
def selectChoice():

    action = request.get_json()["action"]

    availableActions = action["counter"]
    if not availableActions:
        game.phase = "Resolution" if action["general"] else "Challenge"
    else:
        game.phase = "Counter-Action"

    print("action", action)
    return {
        "players": [p.inventory for p in game.players],
        "bank":game.bank,
        "actions": availableActions,
        "player":game.turn,
        "cards":game.cardStack,
        "turn":game.turn,
        "round":game.round,
        "phase":game.phase,
        "activePlayers":game.activePlayers
    }
# Route to process the outcome of a round
# Essentially, on the front-end we'll conduct the entire round and store the decisions made by all the players
# We'll then pass them as paramenters to this route which will resolve the round be returning the winners and losers, as well as the new game state
@app.route("/processRound", methods=["POST"])
@cross_origin()
def processRound():
    global game # Referencing the global variable "game"
    # Resolving the outcome of the round by passing in client parameters. This returns the losers, as well as if there is a need for a a card swap
    losers, exchange, activePlayers, possibleActions = game.outcome(request.get_json()) 
    return {
        "players": [p.inventory for p in game.players],
        "bank":game.bank,
        "actions":possibleActions,
        "cards":game.cardStack,
        # "counterActions":game.counterActions,
        "losers": losers,
        "exchange": exchange,
        "turn":game.turn,
        "round":game.round,
        "phase":game.phase,
        "activePlayers":activePlayers
    }



if __name__ == '__main__':
    app.run()