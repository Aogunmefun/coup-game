
# This is the player class which describes a the main characteristics of each player and what "actions" they have available as well as what is in their "inventory"
# The class also provides a way to add, modify, and remove cards from the players "inventory"




class Player:
    # The initialization of a player is done by passing information about what type of player they are (human or AI), 
    # their "player index" (eg. player1, player2 etc), and their starting cards
    def __init__(self, human, index): 
        self.human = human
        self.index = index
        self.inventory = {
            "coins":0,
            "cards":[

            ]
        }
    
    def addCard(self, card):
        self.inventory["cards"].append(card)

    def removeCard(self, cardIndex):
        self.inventory["cards"].pop(cardIndex)

    def flipCard(self, cardIndex):
        self.inventory["cards"][cardIndex]["flipped"] = True
    
    def addCoins(self, coins):
        self.inventory["coins"] += coins

    def removeCoins(self, coins):
        self.inventory["coins"] -= coins
