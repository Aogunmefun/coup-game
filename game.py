# This is the "Game" class that contains all the methods that affect the game state
# It imports the "Player" class which allows us to simplify code and make it a little cleaner and modular
# Basically, the "Player" class is a class of its own which has methods that impact the state of the individual player
# The "Game" class can then focus on logic that affects the entire game


from cards import cards # Import the "cards" dictionary to allow access to all card types
import player # Import the "Player" class to help abstract lower level player logic
import random

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
            self.players[i].addCard(self.cardStack[rand])
            self.cardStack.pop(rand)
            rand = random.randint(0, len(self.cardStack)-1)
            self.players[i].addCard(self.cardStack[rand])
            self.cardStack.pop(rand)
        
        self.actions = [
           {
               "name": "Tax",
               "description":"Take 3 coins from the Treasury."
           },
           {
               "name":"Assassinate",
               "description":"Pay 3 coins to the Treasury and launch an assassination against another player. If successful that player immediately loses an influence. (Can be blocked by the Contessa)"
           },
           {
               "name":"Steal",
               "description":"Take 2 coins from another player. If they only have one coin, take only one. (Can be blocked by the Ambassador or the Captain)"
           },
           {
               "name":"Exchange",
               "description":"Exchange cards with the Court. First take 2 random cards from the Court deck. Choose which, if any, to exchange with your face-down cards. Then return two cards to the Court deck."
           }
                     
        ]

        self.counterActions = [
            {
                "name":"Block Foreign Aid",
                "description":"Any player claiming the Duke may counteract and block a player attempting to collect foreign aid. The player trying to gain foreign aid receives no coins that turn"
            },
            {
                "name":"Block Assassination",
                "description":"The player who is being assassinated may claim the Contessa and counteract to block the assassination. The assassination fails but the fee paid by the player for the assassin remains spent"
            },
            {
                "name":"Block Stealing",
                "description":"The player who is being stolen from may claim either the Ambassador or the Captain and counteract to block the steal. The player trying to steal receives no coins that turn"
            }
        ]

    # Most important function in game logic. This decides the outcome of each round
    # "decisions" represents a json object (dictionary) of the three different choices (action, counter-action, or challenge) and the associated players who made those choices
    # The way it works is that we first check for a challenge (either on the action or the counter-action)
    def outcome(self, decisions):

        losers = [] # Variable to store the player index that represents the loser of the challenge
        exchange = False

        # Let's deduct any money that needs to be deducted for the action (money is deducted whether the action suceeds or not)
        if decisions["action"]["name"] == "Assassinate": # If the action name is assassinate
            playerInitiatorIndex = decisions["action"]["player"] # Find the index of the player requesting the action
            self.players[playerInitiatorIndex].inventory["coins"] -= 3 # subtract the required number of coins from their inventory
            self.bank += 3 # Add the coins back to the bank


        # Deal with any challenges first
        if decisions["challenge"]:
            print("Evaluating Challenge...")
            playerTargetIndex = decisions["challenge"]["target"]
            playerTargetAction = decisions["action"]["name"] if decisions["action"]["player"] == playerTargetIndex else decisions["counterAction"]["name"]
            playerTagetCardFlipOption = decisions["action"]["cardFlip"] if decisions["action"]["player"] == playerTargetIndex else decisions["counterAction"]["cardFlip"]
            playerInitiatorIndex = decisions["challenge"]["player"]
            succ = True
            for playerCard in self.players[playerTargetIndex].inventory["cards"]:
                if playerTargetAction in playerCard["actions"] or playerTargetAction in playerCard["counter-actions"]:
                    succ = False
            if succ:
                # self.players[playerTargetIndex].inventory["cards"][playerTagetCardFlipOption]["flipped"] = True 
                losers.append(playerTargetIndex)
            else:
                # self.players[playerInitiatorIndex].inventory["cards"][decisions["challenge"]["cardFlip"]]["flipped"] = True
                losers.append(playerInitiatorIndex)
            print("loser", losers)



        # Deal with Actions and Counter Actions Second
        if decisions["counterAction"] and decisions["counterAction"]["player"] not in losers:
            print("Evaluating Counter Action....")
            playerTargetIndex = decisions["counterAction"]["target"]
            playerTargetAction = decisions["action"]["name"]
            playerInitiatorIndex = decisions["counterAction"]["player"]
        if decisions["action"] and decisions["action"]["player"] not in losers:
            if decisions["action"]["name"] == "Tax":
                self.players[decisions["action"]["player"]].addCoins(3)
                self.bank -= 3
            elif decisions["action"]["name"] == "Assassinate":
                losers.append(decisions["action"]["target"])
            elif decisions["action"]["name"] == "steal":
                if self.players[decisions["action"]["player"]].inventory["coins"] == 1:
                    self.players[decisions["action"]["player"]].addCoins(1)
                    self.players[decisions["action"]["target"]].removeCoins(1)
                else:
                    self.players[decisions["action"]["player"]].addCoins(2)
                    self.players[decisions["action"]["target"]].removeCoins(2)
            elif decisions["action"]["name"] == "Exchange":
                exchange = True
            elif decisions["action"]["name"] == "Income":
                self.players[decisions["action"]["player"]].addCoins(1)
                self.bank -= 1
            elif decisions["action"]["name"] == "Foreign Aid":
                self.players[decisions["action"]["player"]].addCoins(2)
                self.bank -= 2
            elif decisions["action"]["name"] == "Coup":
                self.players[decisions["action"]["player"]].removeCoins(7)
                self.bank += 7
                losers.append(decisions["action"]["target"])

        return losers, exchange
            



        # print(decisions["action"])


# game = Game(copiesPerCard=3, startingCoins=request.get_json()["startingCoins"], numPlayers=request.get_json()["numPlayers"])