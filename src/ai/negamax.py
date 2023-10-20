from math import inf

from .move_ordering import order_moves


class Negamax:
    def negamax(self, node, depth: int = inf, alpha: int = -inf, beta: int = inf):
        if depth == 0 or node.is_terminal:
            negation = -1 if node.turn else 1
            return negation * self.score(node), None

        value = -inf

        moves = node.get_legal_moves()
        moves = order_moves(moves)

        for move in moves:
            node.make_move(move)
            new_value, _ = self.negamax(node, depth - 1, -beta, -alpha)
            new_value = -new_value
            if new_value > value:
                value = new_value
                best_move = move
            alpha = max(alpha, value)
            node.undo_move(move)
            if alpha >= beta:
                break
        return value, best_move

    def score(self, node):
        if node.is_win(0):
            return 22 - node.player0_bitboard.bit_count()
        if node.is_win(1):
            return node.player1_bitboard.bit_count() - 22
        return 0  # Draw
