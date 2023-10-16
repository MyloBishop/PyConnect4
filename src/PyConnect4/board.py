"""Allow for clearing the terminal and checking os type."""
import os
from typing import List, Optional

from termcolor import colored


class Connect4Board:
    """
    Represents the game board for Connect 4.
    Allowing for making moves, checking for terminal conditions and displaying the board.
    """

    bitboard_index_to_2d = [
        [5, 12, 19, 26, 33, 40, 47],
        [4, 11, 18, 25, 32, 39, 46],
        [3, 10, 17, 24, 31, 38, 45],
        [2, 9, 16, 23, 30, 37, 44],
        [1, 8, 15, 22, 29, 36, 43],
        [0, 7, 14, 21, 28, 35, 42],
    ]

    def __init__(
        self, width: int = 7, height: int = 6, *, position: Optional[str] = None
    ):
        """
        .  .  .  .  .  .  .
        05 12 19 26 33 40 47  | Numbers represent the index into the full left padded string
        04 11 18 25 32 39 46
        03 10 17 24 31 38 45  | A bit shift left 8 represents movement left across the board
        02 09 16 23 30 37 44  | A bit shift right 8 represents movement right across the board
        01 08 15 22 29 36 43  | A bit shift left 1 represents movement down the board
        00 07 14 21 28 35 42  | A bit shift right 1 represents movement up the board

        Numbers represent the index into the full left padded string

        Player 0 is the player who makes the first move.
        Player 1 is the player who makes the second move.

        Args:
            position (str, optional): 1-based column indexes to make moves in. Defaults to None.
        """
        if width <= 3 or width > 10:  # > 10 as 10 is invalid input into position string
            raise ValueError("Width must be between 4 and 10.")
        if height <= 3:
            raise ValueError("Height must be greater or equal to 4.")

        # Set the width and height of the board
        self.width = width
        self.height = height
        self.padded_height = height + 1  # Height of the board with padding

        # Initialize the game board using bitboards.
        self.player0_bitboard = 0
        self.player1_bitboard = 0
        self.turn = 0  # 0 for player0, 1 for player1

        # ! These can probably be optimised with binary operations but they are only calculated once
        # 1s indicate the lowest free position in each column
        self.bottom_mask = int(("1" + "0" * self.height) * self.width, 2)
        # Mask of the top of each column
        self.top_of_columns = int(("0" * self.height + "1") * self.width, 2)

        self.player0_piece = colored("●", "red")
        self.player1_piece = colored("●", "yellow")

        if position:
            self.setup_position(position)

    @property
    def is_draw(self) -> bool:
        """
        Check if the current game state is a draw.

        Returns:
            bool: True if the current game state is a draw, False otherwise
        """
        # If the top of each column is full mask should evaluate to 0
        return not self.bottom_mask ^ self.top_of_columns

    def print_bitboard(self, bitboard: int):
        """
        Prints the given bitboard in the terminal.
        First bit is printed on the bottom left, then the next bit above it etc.
        Every column has an extra bit at the top to indicate a full column.

        Args:
            bitboard (int): Binary / Integer representation of the bitboard.
        """
        lines = []
        bitboard_str = bin(bitboard)[2:].zfill(self.width * self.padded_height)
        for _ in range(self.width):
            line = bitboard_str[:: self.padded_height]  # Get next bit in row
            bitboard_str = bitboard_str[
                1:
            ]  # Remove the starting bit of the slice sequence of the line
            lines.append(line)
        for line in reversed(lines):  # Print the lines in reverse order
            print(line)
        print()

    def setup_position(self, position: str):
        """
        Sets up the board to the given position.
        The position is a list of moves in order.
        Each move in position is the 1 based index of the column to make a move in.

        Args:
            position (str): Sting of numbers representing column indexes to make moves in
        """
        for index, move in enumerate(position):
            intmove = int(move)
            if not self.is_valid_move(intmove):
                raise ValueError(
                    f"Invalid move {move} at index {index} in position {position}."
                )
            self.make_move(intmove)

    def is_valid_move(self, column: int) -> bool:
        """
        Check if the specified column is a valid move.
        This is done by seeing if the lowest free position is at the "false top" of the column.

        Args:
            column (int): 0-based index of the column to make a move in

        Returns:
            bool: True if the move is valid, False otherwise
        """
        # TODO: Add tests for different widths and heights ensuring bitboard is correct
        top_of_selected_column = 0b1 << (
            (self.width - column - 1) * (self.padded_height)
        )  # Mask of the cell at the top of the column in padded height
        return not bool(self.bottom_mask & top_of_selected_column)

    def make_move(self, column: int):
        """
        Uses bitboards to make a move in the specified column for the given player.
        Bitwise operations are used to update the bitboards and the lowest free position.

        Args:
            column (int): 0-based index of the column to make a move in
        """
        column_mask = 2**self.padded_height - 2 << (
            (self.width - column - 1) * self.padded_height
        )  # Mask with all 1s in the column
        move_mask = (
            self.bottom_mask & column_mask
        )  # 1 in bitboard in the lowest free position in the column
        new_top_cell = move_mask >> 1  # Cell above dropped piece

        self.bottom_mask ^= move_mask | new_top_cell  # Update the lowest free position

        if not self.turn:  # player = 0
            self.player0_bitboard |= move_mask  # Make the move on player0's bitboard
        else:  # player = 1
            self.player1_bitboard |= move_mask  # Make the move on player1's bitboard

        self.turn = self.turn ^ 1  # Switch turns

    def undo_move(self, column: int):
        """
        Undoes the last move made by a player in the specified column.
        Bitwise operations are used to update the bitboards and the lowest free position.

        Args:
            column (int): 0-based index of the column to undo the move in
        """
        # TODO: Really crucially needs to be tested and profiled
        column_mask = 2**self.padded_height - 1 << (
            (self.width - column - 1) * self.padded_height
        )  # Mask with all 1s in the column including the padded top to allow undoing the top cell
        new_top_cell = (
            self.bottom_mask & column_mask
        )  # The top cell in the column before the undo
        old_move = new_top_cell << 1  # The move that is being undone

        self.bottom_mask ^= new_top_cell | old_move  # Update the lowest free position

        if self.turn:  # player = 0
            self.player0_bitboard ^= old_move  # Undo the move on player0's bitboard
        else:  # player = 1
            self.player1_bitboard ^= old_move  # Undo the move on player1's bitboard

        self.turn = self.turn ^ 1  # Revert turn to the player who made the move

    def get_legal_moves(self) -> List[int]:
        """
        Returns a list of valid moves for the current player.
        By checking if each possible column is a valid move.

        Returns:
            list[int]: List of 0-based indexes of columns that are valid moves
        """
        legal_moves = [
            column for column in range(0, self.width) if self.is_valid_move(column)
        ]  # Loop through each column and check if it is a valid move
        return legal_moves

    def is_win(self, player: int) -> bool:
        """
        Check if the game is won for the given player.

        The first operation ensures continuity along the connection.
        Piece is "removed" before the second operation if it doesn't have a left adjacent piece.
        The second operation checks if there are 4 pieces in a row.
        This is done by checking if there is a piece 2 positions away from the second piece.
        There are 4 pieces in a row if there is a 1 in the final bitboard.

        This evaluation is done for each direction (horizontal, vertical, diagonal, anti-diagonal).

        Example for horizontal direction:

        Invalid
        1101000 -> 0100000 -> 0000000

        Valid
        1111000 -> 0111000 -> 0001000

        Args:
            player (int): Player to evaluate win for. 0 for player0, 1 for player1.

        Returns:
            bool: True if the game is won for the given player, False otherwise
        """
        if not player:  # player = 0
            board = self.player0_bitboard
        else:  # player = 1
            board = self.player1_bitboard

        # Check for four-in-a-row in the diagonal direction (top-left to bottom-right)
        diagonal_mask = board & (board >> 7)
        if diagonal_mask & (diagonal_mask >> 2 * 7):
            return True

        # Check for four-in-a-row in the horizontal direction
        horizontal_mask = board & (board >> 8)
        if horizontal_mask & (horizontal_mask >> 2 * 8):
            return True

        # Check for four-in-a-row in the diagonal direction (top-right to bottom-left)
        anti_diagonal_mask = board & (board >> 9)
        if anti_diagonal_mask & (anti_diagonal_mask >> 2 * 9):
            return True

        # Check for four-in-a-row in the vertical direction
        vertical_mask = board & (board >> 1)
        if vertical_mask & (vertical_mask >> 2):
            return True

        return False

    def display(self, *, clear: bool = True):
        """
        Displays the current board state in the terminal to the user.

        Args:
            clear (bool, optional): If True, clears the terminal before display. Defaults to True.
        """
        # Clear the terminal
        if clear:
            os.system("cls" if os.name == "nt" else "clear")

        # Convert bitboard to string of 0s and 1s
        first_player_bitstr = bin(self.player0_bitboard)[2:].zfill(
            self.width * self.padded_height
        )
        second_player_bitstr = bin(self.player1_bitboard)[2:].zfill(
            self.width * self.padded_height
        )

        # Combine both player bitboards into a single board with formatting
        combined_board = [
            self.player0_piece
            if p == "1"
            else (self.player1_piece if a == "1" else " ")
            for p, a in zip(first_player_bitstr, second_player_bitstr)
        ]

        print("╔" + "═══╦" * (self.width - 1) + "═══╗")  # Top border

        # Prints the index of every corresponding cell in the combined board
        for i, row in enumerate(Connect4Board.bitboard_index_to_2d):
            if i > 0:  # No separator on first row
                print("\n╠" + "═══╬" * (self.width - 1) + "═══╣")
            print("║", end=" ")
            print(" ║ ".join([combined_board[cell] for cell in row]), end=" ║")

        print("\n╚" + "═══╩" * (self.width - 1) + "═══╝")  # Bottom border
        print("  1   2   3   4   5   6   7")  # Column numbers
