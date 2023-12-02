# coup-game

This is a repository that aims to replicate the standard board game known as Coup

# Structure

[main.py] Is where the main application logic and back-end flask server sits

[player.py] Is where the player class is defined

[cards.py] Is where the details of each card are stored

# Why this Structure

To be honest, I could've put most of the game logic into one file and called it a day, but I think the point of the excercise is to see how a prospective developer 
likes to structure and write code as well as how they solve problems. 

Personally, I lean towards the modular side of things so that your'e only ever working on one small slice at a time. This means that if
something is wrong, you can quickly debug it without scrolling and parsing through a bunch of logic just to get to realize what the source of the problem is.
It also makes changes to code easier because a change in how a module works doesn't break your whole application except the section that specifically uses a feature.

# Ways to improve

There's obviously ways to improve this design and I tried to address them by how I structured the code.

I've already made the code modular which would make it easy to add either new classes of cards, or new actions/counter-actions players can take without
changing any of the actual game logic. So let's move on to what I actually think could be improved:

1. It's probably not neccesary for each "Player" class to hold on to the entire properties of each card that they have in their "inventory".
In the program, I simply added each cards entire structure (dictionary) to the inventory array. This makes it easier for now since we don't
need to do an extra lookup to determine what the possible actions of the player are (we can just look at the inventory which contains all the details of each card they own).
However, this is extra space and memory that the program needs to allocate during runtime and would affect performace once you get to a complex game where each of
those cards have 100's of actions. In this case you wouldn't want to store 100's of those actions each time the player adds that card to his inventory. Instead what you can
do is store all cards and actioins in one file and just store a reference to the card in the players "inventory". It means an extra lookup, but it saves space and memory

2. There are a few assumptions made here for simplicity, which would not be appropreate during actual development. For example, assuming that

3. I put some logic on the UI side, namely the conduction of a round. Basically, instead of having the back-end receive and deal with the individual descisions that each player makes (i.e. action, counter-action, and challenge), I batch all the decisions made in a round in the front-end and send that to the back-end. While again for a simple app, this is fine, for a more complex game, or perhaps if your'e playing online with other people, this would not be advised.




# Installation Instructions



