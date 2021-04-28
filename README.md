# Finite State Machine and A* Pathfinding
A Pygame application showcasing a finite state machine and A* Pathfinding for the creation of a simple enemy AI.

## How to Use
If you want to test the showcase, you can either:
* 1: Boot up an editor and run the main.py script to get a pygame pop-up and text in the terminal.
* 2: Call the main.py script from a command line for the same result as *1*.
* 3: Download the current release and run the *"finite_a_star_machine.exe"* to get the pygame popup window with the game.

## Screenshots
The showcase is rather simple, with a red square indicating an enemy patrolling accross the map, 
while a blue rectangle indicating the player can be moved by right clicking somewhere on the black ground.
The light gray rectangles indicate "walls" which cannot be passed, and the move is executed with that in mind.

<p float="left">
  <img src="images/enemy.PNG" width ="250"> 
  <img src="images/player.PNG" width="250">
</p>

If the game is run using the main.py file in an editor or through console commands, the following
are potential outputs in the console depending on what the enemy is doing:

![](images/console.PNG)


## Known Issues
This simiplified showcase doesn't support moving while a move is being executed, so while the enemy will react to the player being in its proximity, the player has to wait for the enemy to finish its entire move before being able to move itself.
This also results in the game window likely becomming unresponsive if an input is given while it is currently executing a move.
