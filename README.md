# PyConnect4

This Python implementation represents a Connect 4 game board, offering a robust set of actions to efficiently manage and manipulate the board. It is designed to facilitate the development of Connect 4 AI programs and to provide an interface for playing the game. 

## Table of Contents
- [PyConnect4](#pyconnect4)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Initialization](#initialization)
  - [Game State Properties](#game-state-properties)
  - [Methods](#methods)
  - [License](#license)

## Features

1. **Efficient Bitboard Representation**: The program uses a bitboard-based approach to efficiently represent the game board, making it suitable for AI development.

2. **Making Moves**: The code allows for making moves by specifying the column index, automatically updating the board and the player's turn.

3. **Legal Move Validation**: It can check for valid moves and only allows moves in non-full columns, ensuring the game rules are followed.

4. **Game State Evaluation**: The implementation can evaluate game states, checking for wins, draws, or terminal conditions.

5. **Scoring**: The `score` method provides a score for the current game state, facilitating AI strategies.

6. **Undo Moves**: You can undo the last move made, which can be helpful for various applications, including AI development.

7. **Displaying the Board**: The program includes a visual display of the board in the terminal using colored ASCII characters.

## Initialization

You can create a Connect 4 board instance by initializing the `Board` class. Here's an example:

```python
from PyConnect4 import Board

# Create a new Connect 4 board
board = Board()

# Alternatively, you can initialize a board with a specific game position
position = "1234567776"
board = Board(position)
```

## Game State Properties

- `last_move`: Represents the column index of the last move made in the current game. This property can be helpful for analyzing the game's progress or monitoring the last move.

- `move_count`: Indicates the total number of moves made in the current game. It can be used to track the progression of the game and check for conditions like a draw.

- `turn`: An instance variable that keeps track of the current player's turn. It is set to 0 for Player 1 and 1 for Player 2. This variable is automatically updated after each move and is useful for managing turn-based gameplay.

## Methods

- `get_legal_moves()`: Returns a list of valid moves for the current player.

- `is_valid_move(column)`: Checks if the specified column is a valid move.

- `is_draw()`: Checks if the current game state is a draw.

- `is_terminal()`: Checks if the current game state is a terminal state.

- `is_win(player)`: Checks if the game is won for the given player.

- `make_move(column)`: Makes a move in the specified column.

- `undo_move()`: Undoes the last move made by a player.

- `score()`: Returns the [score](http://blog.gamesolver.org/solving-connect-four/02-test-protocol/#:~:text=Position%E2%80%99s%20score,of%20your%20score.) of the current position

- `display()`: Displays the current board state in the terminal. By default clears the terminal however can be disabled by calling with clear=False.

Example usage:

```python
# Make a move in column 3
board.make_move(3)

# Display the current board state
board.display(clear=False) # Don't clear the terminal

# Undo the last move
board.undo_move()
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
Feel free to use this code as a foundation for your Connect 4 projects, and adapt it as needed for your specific use case. Enjoy building and playing Connect 4!
