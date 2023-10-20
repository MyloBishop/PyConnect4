from math import inf

from .move_ordering import order_moves


class Negamax:
    def negamax(self, node, alpha: int = -inf, beta: int = inf, *, depth: int = inf):
        if depth == 0 or node.is_terminal:
            negation = -1 if node.turn else 1
            return negation * node.score(), None

        value = -inf

        moves = node.get_legal_moves()
        moves = order_moves(moves)

        for move in moves:
            node.make_move(move)
            new_value, _ = self.negamax(node, -beta, -alpha, depth=depth - 1)
            new_value = -new_value
            if new_value > value:
                value = new_value
                best_move = move
            alpha = max(alpha, value)
            node.undo_move(move)
            if alpha >= beta:
                break
        return value, best_move
