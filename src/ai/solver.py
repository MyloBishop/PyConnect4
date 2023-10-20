from math import inf

from .negamax import Negamax


class Solver(Negamax):
    def solve(
        self,
        node: "Board",
        *,
        depth: int = inf,
    ):
        min_score = -(node.width * node.height - node.move_count) // 2
        max_score = (node.width * node.height + 1 - node.move_count) // 2

        while min_score < max_score:
            print(min_score)
            med = min_score + (max_score - min_score) // 2
            if min_score // 2 < med <= 0:
                med = min_score // 2
            elif 0 <= med < max_score // 2:
                med = max_score // 2

            result, _ = self.negamax(node, med, med + 1, depth=depth)

            if result <= med:
                max_score = result
            else:
                min_score = result

        return min_score
