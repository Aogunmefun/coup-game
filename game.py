# This is the "Game" class that contains all the methods that affect the game state
# It's where most of the logic takes place.
# It imports the "Player" class which allows us to simplify code and make it a little cleaner and modular
# Basically, the "Player" class has methods that impact the state of the individual player
# The "Game" class can then focus on logic that affects the entire game


# Import the "cards" dictionary to allow access to all card types
import player # Import the "Player" class to help abstract lower level player logic
import random
from actions import *
from counterActions import *
import json
import copy

cardsFile = open('cards.json')
cards = json.load(cardsFile)

class Game:
    def __init__(self, copiesPerCard: int, startingCoins: int, numPlayers: int):

        # Let's take care of generating the proper number of cards for each class
        # We can take the "copiesPerCard" as the number of each card to spawn
        self.cardStack = []
        for x in range(copiesPerCard):
            for el in cards:
                self.cardStack.append(cards[el])
        random.shuffle(self.cardStack) # Let's mix up the cards

        # Initialize starting coins in the bank
        self.bank = startingCoins

        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player(False, i)) # Initialize a player
            self.players[i].inventory["coins"] += 2 # Give them 2 coins
            self.bank -=2 # Take 2 coins from the bank
            rand = random.randint(0, len(self.cardStack)-1)
            self.players[i].addCard(copy.copy(self.cardStack[rand]))
            self.cardStack.pop(rand)
            rand = random.randint(0, len(self.cardStack)-1)
            self.players[i].addCard(copy.copy(self.cardStack[rand]))
            self.cardStack.pop(rand)
        
        self.round = 1 # Variable representing the current round
        self.turn = 0  # This is the index of the player who's turn it currently is
        self.phase = "Action" # This represents the phase of the game ('action available' (1), 'counter action available' (2), 'challenge available (3))
        self.activePlayers = [0, 1, 2, 3]


    # Most important function in game logic. This decides the outcome of each round
    # There are a maximum of 3 different choices that can happen (action, counter-action, and challenge)
    # "decisions" represents a json object (dictionary) sent from the front-end of those choices and the associated players who made those choices. Example json object below
    # {
    #     "action": {
    #         "player":0, This represents the index of the player that made the choice
    #         "name":"Assassinate", This represents the name of the choice that was made (eg. assassinate, steal etc.)
    #         "cardFlip":1,
    #         "target":1, This represents the target of the choice that was made (if there was one)
    #     },
    #     "counterAction":{
    #         "player":1,
    #         "cardFlip":1,
    #         "target":0,
    #         "name":"Block Assassination"
            
    #     },
    #     "challenge": {
    #         "player": 2,
    #         "cardFlip":0,
    #         "target":0
    #     }
    # }
    # The way it works is that we first check for a challenge (either on the action or the counter-action)
    # Then we deal with the counter-action and action
    # The "losers" array will store the index of players who lost influence and need to have their cards flipped (either by losing a challenge, or being the target of an action)
    def outcome(self, decisions):
        print("decisions", decisions)

        losers = [] # Variable to store the player index's that represents the players who lost influence
        exchange = False

        # Let's deduct any money that needs to be deducted for the action (money is deducted whether the action suceeds or not)
        # In this case, only assassinations require money to be spent
        if decisions["action"]["name"] == "Assassinate": # If the action name is assassinate
            playerInitiatorIndex = decisions["action"]["player"] # Find the index of the player requesting the action
            self.players[playerInitiatorIndex].inventory["coins"] -= 3 # subtract the required number of coins from their inventory
            self.bank += 3 # Add the coins back to the bank


        # Deal with any challenges first
        if decisions["challenge"]: # Check if the "challenge" field is populated (i.e. a challenge was made) 
            print("Evaluating Challenge...")
            playerTargetIndex = decisions["challenge"]["target"] # Index of the Target for the "challenge"
            # Figuring out the name of the choice the target player made (e.g. assasinate, block stealing etc.)
            # Let's try to match the targetted player's index with the index of the player who either made an "action" or "counter-action"
            playerTargetChoiceName = decisions["action"]["name"] if decisions["action"]["player"] == playerTargetIndex else decisions["counterAction"]["name"]
            playerInitiatorIndex = decisions["challenge"]["player"] # The index of the player making the "challenge"
            succ = True # Assume challenge is successful until proven otherwise
            for playerCard in self.players[playerTargetIndex].inventory["cards"]: # Iterate through target players card list and see if they have the right cards
                if (playerTargetChoiceName in playerCard["actions"] or playerTargetChoiceName in playerCard["counterActions"]) and not playerCard["flipped"]:
                    succ = False
            if succ:
                losers.append(playerTargetIndex) # If successful, add the target player to the "losers" array
                self.players[playerTargetIndex].flipCard(0 if 1 in self.players[playerTargetIndex].getFlipped() else 1)
                # self.players[playerTargetIndex].flipCard(0)
                # print("Challenge Successful", playerTargetIndex, playerInitiatorIndex, self.players["cards"])
                print("Challenge Successful...")
            else:
                losers.append(playerInitiatorIndex) # If unsuccessful, add the player who challenged to the "losers" array 
                self.players[playerInitiatorIndex].flipCard(0 if 1 in self.players[playerInitiatorIndex].getFlipped() else 1)
                # self.players[playerInitiatorIndex].flipCard(0)
                # print("Challenge Failed",, self.players[1].inventory["cards"], self.players[2].inventory["cards"])
                print("Challenge Failed...")
            print(self.players[0].inventory["cards"])
            print(self.players[1].inventory["cards"])
            print(self.players[2].inventory["cards"])
            print("stak", self.cardStack)


        # Deal with Actions and Counter Actions Second
        if decisions["counterAction"] and decisions["counterAction"]["player"] not in losers: # If there is a "counter-action" and the player is not in the "losers" variable
            # If a "counter-action" is successful, there's nothing else to be done. The action is automatically blocked by the if-else statement, and we've already accounted for lost coins
            pass
        else: # If there was no "counter-action" or the player who made it was in the "losers" array, then the action has to proceed
            if decisions["action"] and decisions["action"]["player"] not in losers: # Making sure that there actually was an action done and that the player making it didn't lose a challenge
                if decisions["action"]["name"] == "Tax": # If the action name was Tax
                    self.players[decisions["action"]["player"]].addCoins(3) # Add coins to player
                    self.bank -= 3 # Take coins from bank
                elif decisions["action"]["name"] == "Assassinate": # If action name was Assassinate
                    losers.append(decisions["action"]["target"]) # Add the targeted player to the "losers" array, since the target player needs to lose an influence point
                    self.players[decisions["action"]["target"]].flipCard(0 if 1 in self.players[decisions["action"]["target"]].getFlipped() else 1)
                elif decisions["action"]["name"] == "Steal": # If action name was steal
                    if self.players[decisions["action"]["player"]].inventory["coins"] == 1: # Making sure there are enough coins in the target players inventory
                        self.players[decisions["action"]["player"]].addCoins(1) # Add only one coin to players inventory since the target player only has one coin to give
                        self.players[decisions["action"]["target"]].removeCoins(1) # Remove coins from target players inventory
                    else: # If the target player has more than one coin
                        self.players[decisions["action"]["player"]].addCoins(2) # Add 2 coins to players inventory 
                        self.players[decisions["action"]["target"]].removeCoins(2) # Remove 2 coins from target players inventory
                # elif decisions["action"]["name"] == "Exchange": # If action name is exchange
                #     exchange = True # Set exchange flag to true
                #     exchangePlayerIndex = decisions["action"]["player"] # Set the index of the player who needs to perform an exchange
                elif decisions["action"]["name"] == "Income": # If action name is income
                    self.players[decisions["action"]["player"]].addCoins(1) # Add one coin to players inventory
                    self.bank -= 1 # Take one coin from bank
                elif decisions["action"]["name"] == "Foreign Aid": # If action name is Foreign Aid
                    self.players[decisions["action"]["player"]].addCoins(2) # Add 2 coins to players inventory
                    self.bank -= 2 # Take 2 coins from bank
                elif decisions["action"]["name"] == "Coup": # If players action name is Coup
                    self.players[decisions["action"]["player"]].removeCoins(7) # Remove 7 coins from players inventory
                    self.bank += 7 # Add 7 coins to the bank
                    losers.append(decisions["action"]["target"]) # Add the target player for the action to the losers array

        # ****************Check to see if any players are out of the game. Iterate through all the players, and check if any of them have more that one card flipped************
        for ind in range(len(self.players)):
            if len(self.players[ind].getFlipped()) > 1 and ind in self.activePlayers:
                self.activePlayers.remove(ind)

        # [0, 1, 2, 3]
        # [0, 3,]

        self.round+=1
        self.turn = self.turn+1 if self.turn < self.activePlayers[-1] else self.activePlayers[0]
        while self.turn not in self.activePlayers:
            self.turn+=1
        
        self.phase = "Action"

        possibleActions = copy.copy(actions)
        playerCoins = self.players[self.turn].inventory["coins"]
        if playerCoins > 10:
            possibleActions = possibleActions[4]
        else:
            for a in possibleActions:
                if a["coins"]>playerCoins:
                    possibleActions.remove(a)
        return losers, exchange, self.activePlayers, possibleActions

