# This is where the main logic of the code is contained.
# A flask server is used to process UI requests from the user
# Additionally, for the UI, a simple React front-end will be used in order to make it a bit more visual (and show off a little)

# The game will be run using a player class that represents a player, their possible desicions, and what their current state is (cards, coins, influence etc)
# The number of player classes that are instantiated are simply based on the number of players (AI and human)
# The Cards will be simple ojects that hold the name of the card, the possible actions, and the possible counter-actions



import player # importing player class
from cards import * # importing cards module to access the different card types
from game import Game
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import json


game = Game(3, 50, 3)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'content-Type'


@app.route("/createGame", methods=["POST"])
def createGame():
    print(request.get_json())
    global game
    # Initializing game and game parameters
    game = Game(copiesPerCard=request.get_json()["cardCopies"], startingCoins=request.get_json()["startingCoins"], numPlayers=request.get_json()["numPlayers"])
    print(game.cardStack, len(game.cardStack))
    
    return {
        "players": [p.inventory for p in game.players],
        # "bank":game.bank,
        # "actions":[{"name": act["name"], "description":act["description"]} for act in game.actions],
        "cards":game.cardStack,
        # "counterActions":game.counterActions
    }


@app.route("/processRound", methods=["POST"])
def processRound():
    global game
    losers, exchange = game.outcome(request.get_json())
    return {
        "players": [p.inventory for p in game.players],
        # "bank":game.bank,
        # "actions":[{"name": act["name"], "description":act["description"]} for act in game.actions],
        "cards":game.cardStack,
        # "counterActions":game.counterActions,
        "losers": losers,
        "exchange": exchange
    }







if __name__ == '__main__':
    app.run()