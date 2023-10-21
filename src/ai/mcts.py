import math
import random
from copy import deepcopy
from typing import Type

from ai import Node
from board import Board


class MonteCarloTreeSearch:
    """
    The Monte Carlo Tree Search (MCTS) algorithm.
    """

    def __init__(
        self,
        root_state: Type[Board],
        exploration_weight: float = math.sqrt(2),
        iterations: int = 1000,
    ):
        """
        Initialize the MCTS algorithm.

        Args:
            root_state: The initial game state.
            exploration_weight (float): The UCT exploration weight.
            iterations (int): The number of iterations (simulations) to run.
        """
        self.root = Node(root_state)
        self.exploration_weight = exploration_weight
        self.iterations = iterations

    def search(self):
        """
        Run the MCTS algorithm for a specified number of iterations.
        """
        for _ in range(self.iterations):
            node_to_expand = self.select()
            result = self.simulate(node_to_expand)
            self.backpropagate(node_to_expand, result)

    def select(self):
        """
        Selection step: Traverse the tree to select a node for expansion.

        Returns:
            Node: The selected node.
        """
        node = self.root
        while not node.state.is_terminal:
            if not node.is_fully_expanded():
                # Expand if not all children have been created
                child = self.expand(node)
                return child
            node = node.select_child(self.exploration_weight)
        return node

    def expand(self, parent_node):
        """
        Expansion step: Create and add a child node to the tree.

        Args:
            parent_node (Node): The parent node to expand.

        Returns:
            Node: The newly created child node.
        """
        legal_moves = parent_node.state.get_legal_moves()
        move = random.choice(legal_moves)  # Randomly select a legal move
        new_state = deepcopy(parent_node.state)  # Create a copy of the game state
        new_state.make_move(move)  # Apply the selected move
        new_child = Node(new_state, parent=parent_node)
        parent_node.add_child(new_child)
        return new_child

    def simulate(self, node_to_expand):
        """
        Simulation step: Simulate a game from the selected node to a terminal state.

        Args:
            node_to_expand (Node): The node from which to start the simulation.

        Returns:
            float: The result of the simulation (1.0 for a win, 0.0 for a draw, -1.0 for a loss).
        """
        state = deepcopy(node_to_expand.state)
        while not state.is_terminal:
            legal_moves = state.get_legal_moves()
            move = random.choice(legal_moves)  # Randomly select a legal move
            state.make_move(move)
        return state.get_result(
            node_to_expand.state.current_player
        )  # Get the result from the perspective of the expanding player

    def backpropagate(self, node_to_expand, result):
        """
        Backpropagation step: Update visit counts and values along the path to the root.

        Args:
            node_to_expand (Node): The node from which the result was obtained.
            result (float): The result of the simulation.
        """
        while node_to_expand is not None:
            node_to_expand.update(result)
            node_to_expand = node_to_expand.parent

    def get_best_move(self):
        """
        Get the best move based on the accumulated statistics in the tree.

        Returns:
            int: The index of the best move.
        """
        if not self.root.children:
            return None
        best_child = self.root.get_best_child()
        return best_child.state.get_last_move()
