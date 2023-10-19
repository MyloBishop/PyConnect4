from math import inf

from board import Board


def negamax(node, depth: int = inf, alpha: int = -inf, beta: int = inf):
    if depth == 0 or node.is_terminal:
        negation = -1 if node.turn else 1
        return negation * score(node), None

    value = -inf
    moves = node.get_legal_moves()
    moves = order_moves(moves)

    for move in moves:
        node.make_move(move)
        new_value, _ = negamax(node, depth - 1, -beta, -alpha)
        new_value = -new_value
        if new_value > value:
            value = new_value
            best_move = move
        alpha = max(alpha, value)
        node.undo_move(move)
        if alpha >= beta:
            break
    return value, best_move


def order_moves(moves):
    # Center column first, then head outwards
    center = 3
    moves.sort(key=lambda move: abs(move - center))
    return moves


def score(node):
    if node.is_win(0):
        return 22 - node.player0_bitboard.bit_count()
    if node.is_win(1):
        return node.player1_bitboard.bit_count() - 22
    return 0  # Draw


root = Board(position="11233566724171221527127745")
root.display()
print(negamax(root))
