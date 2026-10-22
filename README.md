# Checkers Game

A console-based Checkers game built with Python, where a human plays against a computer opponent.

## Features
- Legal move validation, captures, and promotion to kings.
- Computer opponent that looks for winning moves, avoids immediate losses, and prioritizes captures and promotions.
- Input validation and game-over detection.
- Object-oriented design with separate domain, service, and UI layers.
- Unit tests for the board, game rules, and computer strategy.

## Run
Requires Python 3.9 or newer. No additional packages are needed.

```sh
python3 main.py
```

Follow the instructions in the console to choose your moves.

## Tests
```sh
python3 -m unittest discover -s tests -v
```

## Project structure
- `checkers/domain/` - board, pieces, moves, and rules
- `checkers/services/` - game state and computer strategy
- `checkers/ui/` - console interface
- `tests/` - unit tests
- `main.py` - application entry point

## About
Academic project for the Fundamentals of Programming course at Babes-Bolyai University.
