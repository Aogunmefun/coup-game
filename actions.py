actions = [
    {
        "name": "Tax",
        "description":"Take 3 coins from the Treasury.",
        "general":False,
        "targeted":False,
        "counter":[],
        "coins":0
    },
    {
        "name":"Assassinate",
        "description":"Pay 3 coins to the Treasury and launch an assassination against another player. If successful that player immediately loses an influence. (Can be blocked by the Contessa)",
        "general":False,
        "targeted":True,
        "counter":["Block Assassination"],
        "coins":3
    },
    {
        "name":"Steal",
        "description":"Take 2 coins from another player. If they only have one coin, take only one. (Can be blocked by the Ambassador or the Captain)",
        "general":False,
        "targeted":True,
        "counter":["Block Stealing"],
        "coins":0
    },
    # {
    #     "name":"Exchange",
    #     "description":"Exchange cards with the Court. First take 2 random cards from the Court deck. Choose which, if any, to exchange with your face-down cards. Then return two cards to the Court deck.",
    #     "general": False
    # },
    {   
        "name":"Income",
        "description":"Take 1 coin from the treasury",
        "general":True,
        "counter":[],
        "coins":0
    },
    # {
    #     "name":"Foreign Aid",
    #     "description":"Take 2 coins from the Treasury"
    # },
    {
        "name":"Coup",
        "description":"Pay 7 coins to the treasury and launch a coup against another player. That player immediately loses an influence. A Coup is always successful. If you start your turn with 10 (or more) coins you are required to launch a Coup",
        "general":True,
        "counter":[],
        "coins":7
    }
                
]