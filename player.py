
# This is the player class which describes a the main characteristics of each player and the contents of their "inventory"
# It effectively monitors the state of each player



class Player:
    # The initialization of a player is done by passing information about what type of player they are (human or AI), 
    # and their "player index" (eg. player1, player2 etc]]]]]
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

    def getFlipped(self):
        res = []
        for ind in range(len(self.inventory["cards"])):
            if self.inventory["cards"][ind]["flipped"]: res.append(ind)
        return res
    
    def addCoins(self, coins):
        self.inventory["coins"] += coins

    def removeCoins(self, coins):
        self.inventory["coins"] -= coins
