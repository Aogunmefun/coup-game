# coup-game

This is a repository that aims to replicate the standard board game known as Coup

# Structure

[main.py] Is where the main application logic and back-end flask server sits

[player.py] Is where the player class is defined

[cards.json] Is where the details of each card are stored

[actions.py] Contains all the actions the players can take

[counterActions.py] Contains all the counter-actions the players can take

[game.py] This is the class that controls the state of the game

# Why this Structure

To be honest, I could've put most of the game logic into one or two files and called it a day, but I think the point of the excercise is to see how a prospective developer 
likes to structure and write code as well as how they solve problems. 

Personally, I lean towards the modular side of things so that your'e only ever working on one small slice at a time. This means that if
something is wrong, you can quickly debug it without scrolling and parsing through a bunch of logic just to get to realize what the source of the problem is.
It also makes changes to code easier because a change in how a module works doesn't break your whole application except the section that specifically uses a feature.

# Ways to improve

There's obviously ways to improve this design and either improve the game as a whole or make the code more clean/efficient.

I've already made the code modular which would make it easy to add either new classes of cards, or new actions/counter-actions players can take without
changing any of the actual game logic. So let's move on to what I actually think could be improved:

1. It's probably not neccesary for each "Player" class to hold on to the entire properties of each card that they have in their "inventory".
In the program, I simply added each cards entire structure (dictionary) to the inventory array. This makes it easier for now since we don't
need to do an extra lookup to determine what the possible actions of the player are (we can just look at the inventory which contains all the details of each card they own).
However, this is extra space and memory that the program needs to allocate during runtime and would affect performace once you get to a complex game where each of
those cards have 100's of actions. In this case you wouldn't want to store 100's of those actions each time the player adds that card to his inventory. Instead what you can
do is store all cards and actioins in one file and just store a reference to the card in the players "inventory". It means an extra lookup, but it saves space and memory

2. There's no need for the large number of separate .py files. I really only did this because of my assumptions at the very beginning. I also left it this way because it was easier than having just 2 files that are 200 lines long for such a small application. This way I could find and change things much more easily. However, the issue isn't really the amount of separate files, but the fact that they are all .py. This takes up too much space and could simply be replaced with a simple json or text file depending on the format of the data. 

3. I put some logic on the UI side, namely the conduction of a round. Basically, instead of having the back-end receive and deal with the individual descisions that each player makes (i.e. action, counter-action, and challenge), I batch all the decisions made in a round in the front-end and send that to the back-end. While again for a simple app, this is fine, for a more complex game, or perhaps if your'e playing online with other people, this would not be advised.

4. The UI is also not responsive, meaning that the contents don't resize to fit on the user's screen. This makes it non suitable for mobile devices (maybe even tablets as well). Of course, this can be fixed by implementing some css queries and adding a few breakpoints.

5. The decisions that the AI makes are randomized meaning that most of their choices would be illogical. Further imporvements would have some rules to dictacte what sort of choices the AI should make. Or one could use something like ChatGPT to decide what action the AI should take



# Installation Instructions

The game runs in two seperate places. One will be the back-end, responsible for the game logic. Second is the front-end which contains the UI for the game. These are all in the  [release] folder.

Inside thes folders, you'll find:

In the [release/server] folder, you will find the back-end server. This is already compiled into an executable file that can be launched simply by double clicking on the file.  

In the [release/ui] folder, you will find the UI. Double click on the "index.html" to open up the GUI in a browser window

PS: Make sure to actually extract the ZIP folder you get from Github otherwise you may see a blank screen

After that, you should be good to go!

