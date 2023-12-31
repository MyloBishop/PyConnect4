import os
from typing import List

from termcolor import colored


class Board:
    """
    Represents the game board for Connect 4.
    Allowing for making moves, checking for terminal conditions and displaying the board.
    """

    # Set the width and height of the board
    WIDTH = 7
    HEIGHT = 6
    PADDED_HEIGHT = HEIGHT + 1
    BITBOARD_SIZE = WIDTH * PADDED_HEIGHT

    # Mask of the top of each column
    TOP_OF_COLUMNS = int(("0" * HEIGHT + "1") * WIDTH, 2)

    def __init__(
        self,
        position: str = "",
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
            position (str, optional): 1-based column indexes to make moves in. Defaults to "".
        """

        if (
            Board.WIDTH <= 3 or Board.WIDTH > 10
        ):  # >10 is invalid as 2+ digit columns are not representable in position string
            raise ValueError("Width must be between 4 and 10.")
        if Board.HEIGHT <= 3:
            raise ValueError("Height must be greater or equal to 4.")

        # Bitboard to 2D index mapping (as seen above)
        self.bitboard_index_to_2d = [
            list(range(count, Board.BITBOARD_SIZE, Board.PADDED_HEIGHT))
            for count in reversed(range(Board.HEIGHT))
        ]

        # Initialize the game board using bitboards.
        self.player0_bitboard = 0
        self.player1_bitboard = 0
        self.turn = 0  # 0 for player0, 1 for player1

        # 1s indicate the lowest free position in each column
        self.bottom_mask = int(("1" + "0" * Board.HEIGHT) * Board.WIDTH, 2)

        # Keep track of game position
        self.position = position

        if position:
            self.setup_position(position)

    @property
    def move_count(self) -> int:
        """
        Return the number of moves made in the current game.

        Returns:
            int: Number of moves made in the current game
        """
        return self.player0_bitboard.bit_count() + self.player1_bitboard.bit_count()

    @property
    def last_move(self) -> int:
        """
        Return the last move made in the current game.

        Returns:
            str: Last move made in the current game
        """
        return int(self.position[-1]) - 1

    def get_legal_moves(self) -> List[int]:
        """
        Returns a list of valid moves for the current player.
        By filtering out moves where there is a bit at the top of the column
        and a bit in the bottom mask at the same position.

        Returns:
            list[int]: List of 0-based indexes of columns that are valid moves
        """
        legal_moves = list(range(Board.WIDTH))

        # If a column is full, there is a bit at the top of the column in both masks
        full_columns_bitboard = self.bottom_mask & Board.TOP_OF_COLUMNS

        if not full_columns_bitboard:  # No full columns
            return legal_moves  # so all columns are valid

        # Efficiently convert the bitboard to a list of non-full columns indexes
        legal_moves = list(
            filter(
                lambda column: not full_columns_bitboard
                & 0b1
                << (
                    (Board.WIDTH - column - 1) * Board.PADDED_HEIGHT
                ),  # Shift a test bit to top of column
                legal_moves,
            )
        )

        return legal_moves

    def is_valid_move(self, column: int) -> bool:
        """
        Check if the specified column is a valid move.
        This is done by seeing if the lowest free position is at the "false top" of the column.

        Args:
            column (int): 0-based index of the column to make a move in

        Returns:
            bool: True if the move is valid, False otherwise
        """
        top_of_selected_column = 0b1 << (
            (Board.WIDTH - column - 1) * (Board.PADDED_HEIGHT)
        )  # Mask of the cell at the top of the column in padded Board.HEIGHT
        return not bool(self.bottom_mask & top_of_selected_column)

    def is_draw(self) -> bool:
        """
        Check if the current game state is a draw.

        Returns:
            bool: True if the current game state is a draw, False otherwise
        """
        # If the top of each column is full, mask evaluates to 0
        return not self.bottom_mask ^ Board.TOP_OF_COLUMNS

    def is_terminal(self) -> bool:
        """
        Check if the current game state is a terminal state.
        Only checks win for the player who made the last move.

        Returns:
            bool: True if the current game state is a terminal state, False otherwise
        """
        return bool(self.is_win(self.turn ^ 1) or self.is_draw)

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
        diagonal_mask = board & (board >> Board.HEIGHT)
        if diagonal_mask & (diagonal_mask >> 2 * Board.HEIGHT):
            return True

        # Check for four-in-a-row in the horizontal direction
        horizontal_mask = board & (board >> (Board.HEIGHT + 1))
        if horizontal_mask & (horizontal_mask >> 2 * (Board.HEIGHT + 1)):
            return True

        # Check for four-in-a-row in the diagonal direction (top-right to bottom-left)
        anti_diagonal_mask = board & (board >> (Board.HEIGHT + 2))
        if anti_diagonal_mask & (anti_diagonal_mask >> 2 * (Board.HEIGHT + 2)):
            return True

        # Check for four-in-a-row in the vertical direction
        vertical_mask = board & (board >> 1)
        if vertical_mask & (vertical_mask >> 2):
            return True

        return False

    def setup_position(self, position: str):
        """
        Sets up the board to the given position.
        The position is a list of moves in order.
        Each move in position is the 1 based index of the column to make a move in.

        Args:
            position (str): Sting of numbers representing column indexes to make moves in
        """
        for index, move in enumerate(position):
            intmove = int(move) - 1
            if not self.is_valid_move(intmove):
                raise ValueError(
                    f"Invalid move {move} at index {index} in position {position}."
                )
            self.make_move(intmove)

    def make_move(self, column: int):
        """
        Uses bitboards to make a move in the specified column for the given player.
        Bitwise operations are used to update the bitboards and the lowest free position.

        Args:
            column (int): 0-based index of the column to make a move in
        """
        column_mask = 2**Board.PADDED_HEIGHT - 2 << (
            (Board.WIDTH - column - 1) * Board.PADDED_HEIGHT
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
        self.position = self.position + str(column + 1)

    def undo_move(self):
        """
        Undoes the last move made by a player
        Bitwise operations are used to update the bitboards and the lowest free position.

        Args:
            column (int): 0-based index of the column to undo the move in
        """
        column = int(self.position[-1] - 1)

        column_mask = 2**Board.PADDED_HEIGHT - 1 << (
            (Board.WIDTH - column - 1) * Board.PADDED_HEIGHT
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
        self.position = self.position[:-1]

    def score(self) -> int:
        """
        Return the score of the current position.

        We define a score for any non final position reflecting the
        outcome of the game for the player to play, considering that
        both players play perfectly and try to win as soon as possible
        or lose as late as possible.

        Returns:
            int: Score of the current position
        """
        if self.is_win(player=0):
            return 22 - self.player0_bitboard.bit_count()
        if self.is_win(player=1):
            return self.player1_bitboard.bit_count() - 22
        return 0  # Draw

    def print_bitboard(self, bitboard: int):
        """
        Prints the given bitboard in the terminal.
        First bit is printed on the bottom left, then the next bit above it etc.
        Every column has an extra bit at the top to indicate a full column.

        Args:
            bitboard (int): Binary / Integer representation of the bitboard.
        """
        lines = []
        bitboard_str = bin(bitboard)[2:].zfill(Board.BITBOARD_SIZE)
        for _ in range(Board.WIDTH):
            line = bitboard_str[:: Board.PADDED_HEIGHT]  # Get next bit in row
            bitboard_str = bitboard_str[1:]  # Start at next bit
            lines.append(line)
        for line in reversed(lines):  # Print the lines in reverse order
            print(line)
        print()

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
        first_player_bitstr = bin(self.player0_bitboard)[2:].zfill(Board.BITBOARD_SIZE)
        second_player_bitstr = bin(self.player1_bitboard)[2:].zfill(Board.BITBOARD_SIZE)

        # Combine both player bitboards into a single board with formatting
        combined_board = [
            colored("●", "red")
            if p == "1"
            else (colored("●", "yellow") if a == "1" else " ")
            for p, a in zip(first_player_bitstr, second_player_bitstr)
        ]

        print("╔" + "═══╦" * (Board.WIDTH - 1) + "═══╗")  # Top border

        # Prints the index of every corresponding cell in the combined board
        for i, row in enumerate(self.bitboard_index_to_2d):
            if i > 0:  # No separator on first row
                print("\n╠" + "═══╬" * (Board.WIDTH - 1) + "═══╣")
            print("║", end=" ")
            print(" ║ ".join([combined_board[cell] for cell in row]), end=" ║")

        print("\n╚" + "═══╩" * (Board.WIDTH - 1) + "═══╝")  # Bottom border
        print(
            " "
            + "  ".join(
                f"{i:2d}" for i in range(1, Board.WIDTH + 1)
            )  # Dynamic column numbers
        )
