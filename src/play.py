from ai import negamax
from board import Board


def player_move(board):
    while True:
        try:
            column = int(input("Enter your move (1-7): ")) - 1
            if 0 <= column < board.width and board.is_valid_move(column):
                return column
            print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number (1-7).")


def main():
    board = Board()

    print("Welcome to Connect 4! You are '●' and the AI is '○'.")
    board.display()

    while not board.is_terminal:
        if board.turn == 0:
            # Player's turn
            column = player_move(board)
        else:
            # AI's turn
            print("AI is thinking...")
            _, column = negamax(board, depth=10)  # Adjust the depth as needed
            print(f"AI chooses column {column + 1}")

        board.make_move(column)
        board.display()

    if board.is_win(0):
        print("Congratulations! You win!")
    elif board.is_win(1):
        print("AI wins! Better luck next time.")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
