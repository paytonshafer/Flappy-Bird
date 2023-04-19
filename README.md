# Flappy Bird
This contains the source code for a flappy bird game that has been implemented in Python using the PyGame library.

## flappybirdgame
This folder contains the code for the whole game of flappy bird. Once the game has been started you are given the option to choose a difficulty, the 
difficulty is decided by the size of the gap between the pipes. 

## flappybirdai
This folder contains a version of flappy bird that uses NEAT to have ai play the game. When the program is ran the ai starts and runs it's trials to try
to create the perfect bird. This part used 'config-feedforward.txt' as the config file for NEAT.

## usage
To run either of the projects just download the source files and cd to the correct folder. There will only be one python file in each folder so that is the
file that needs to be ran. If you are in the flappybirdgame directory, use this command to run:
```sh
python flappybirdgame.py
```
Otherwise, if you are in he flappybirdai directory, use this command to run:
```sh
python flappybirdai.py
```
