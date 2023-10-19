from board import Board


def negamax(node):
    node.display(clear=False)

    if node.is_terminal:
        return score(node)

    value = float("-inf")
    moves = node.get_legal_moves()

    for move in moves:
        node.make_move(move)
        value = max(value, -negamax(node))
        node.undo_move(move)
    return value


def score(node):
    if node.is_win(0):
        print("Player 0 wins")
        return 22 - node.player0_bitboard.bit_count()
    if node.is_win(1):
        print("Player 1 wins")
        return node.player1_bitboard.bit_count() - 22
    print("Draw.")
    return 0  # Draw


root = Board(position="144324431445513573673777361765615215226")
root.display()
print(negamax(root))
