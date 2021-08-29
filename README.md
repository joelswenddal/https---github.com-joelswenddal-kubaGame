# Kuba Game
This Python 3 program implements game play, turn taking, movement, and game state updating for the game Kuba. 

This was created as a portfolio project for an Introductory Programming CS course at my university. The main goal of the project was to demonstrate fundamental skills using object-oriented programming. This was made in a very short period of time, but when I have more time I plan to implement the game with interactive GUI in the web browser using JS and React, which I've been learning in other courses.

## Table of contents

* [General info and rules](#general-info)
* [Gameplay using KubaGame class](#class-methods)
* [Technologies](#technologies)
* [Contact](#contact)

## General info and rules

Kuba takes place on a 7x7 grid using Black, White and Red marbles.

Two players, assigned Black or White marbles, take turns pushing their marbles one
space in any orthagonal direction, as long as the direction they 'push away' from is
an empty spot (the empty space provides 'access' to the marble). 

Any marbles in the direction they are pushing in are moved down by their push (row or column).

Wins happen when a player pushes 7 red marbles off the board, the other player's
marbles (Black or White) are all pushed off the board, or the other player is not able to make any moves.

Full Kuba rules: https://sites.google.com/site/boardandpieces/list-of-games/kuba

Video explaining Kuba rules: https://www.youtube.com/watch?v=XglqkfzsXYc

## Gameplay using KubaGame class
The methods of the KubaGame class implement the core functionality of the Kuba game. Responsibilities of the class include:
  - executing moves
  - conducting move validation according to game rules
  - allotting and tracking turn-taking
  - tracking game state, including win declaration

### Methods:

__Initializing the KubaGame object__: Takes two tuples as parameters, each containing player name and color of the marble that the player is playing (ex: ('PlayerA', 'B'), ('PlayerB','W')). This intializes the board. On the board R, B, W are be used to represent Red, Black and White marbles, and an X represents an empty space. The current state of the board can be displayed visually with the class's print_board method.

The names of players are decided by the users of the game and should always be passed in the same way as it is passed when initializing the KubaGame object. The marbles are always represented as upper case R, B, W in the method calls and the methods use the same representation when returning any relevant values. Similary, X, L, R, F and B, which represent absence of marble and all the four directions respectively, are also in upper case.

__get_current_turn__: returns the player name whose turn it is to play the game

__make_move__: takes three parameters -- playername, coordinates i.e. a tuple containing the location of marble that is being moved, and the direction in which the player wants to push the marble. Valid directions are L(Left), R(Right), F(Forward) and B(Backward)

__get_winner__: returns the name of the winning player. If no player has won yet, it returns None

__get_captured__: takes player's name as parameter and returns the number of Red marbles captured by the player. This returns 0 if no marble is captured.

__get_marble__: takes the coordinates of a cell as a tuple and returns the marble that is present at the location. If no marble is present at the coordinate location return 'X'.

__get_marble_count__: returns the number of White marbles, Black marbles and Red marbles as tuple in the order (W,B,R).

__print_board__: prints a visual of the board updated with its current state.

Regarding the grid coordinates: The top left cell on the board is refered to by (0,0), and the bottom right cell by (6,6). i.e (row_number, col_number)

Movement directions are explained in the following image:

![alt-text](https://user-images.githubusercontent.com/32501313/117386394-b08b1180-ae9b-11eb-9779-9bbd8531c91d.PNG)


A simple example of how the `KubaGame` class can be used:

```
game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B')) 
# initialize game object with two named players as white or black
game.get_marble_count() 
#returns (8,8,13) - 8 White marbles, 8 Black marbles, 13 red marbles
game.get_captured('PlayerA') 
#returns 0
game.get_winner() 
#returns None
game.make_move('PlayerA', (6,5), 'F') 
#Returns True - Successful move forward ('F')
game.make_move('PlayerA', (6,5), 'L') 
#Cannot make this move because of game rule
game.get_marble((5,5)) 
#returns 'W' (White)
```
## Technologies
Python 3

## Contact
For suggestions or questions related to use of this program, please contact me at: joel.swenddal@gmail.com

