"""Enable type annotations for Node class."""
from __future__ import annotations

import math
from typing import List, Optional, Type

from board import Board


class Node:
    """
    A node in the Monte Carlo Tree Search (MCTS) tree.
    """

    def __init__(self, state: Type[Board], parent: Optional[Type[Board]] = None):
        """
        Initialize an MCTS node.

        Args:
            state (Board): The game state associated with this node.
            parent (Node, optional): The parent node. If None, this node is the root node.
        """
        self.state: Type[Board] = state  # The game state associated with this node
        self.parent: Optional[Type[Board]] = parent  # Parent node
        self.children: List = []  # List of child nodes
        self.visits: int = 0  # Number of times this node has been visited
        self.value: int = 0  # Total value accumulated from this node

    def is_fully_expanded(self) -> bool:
        """
        Check if all possible child nodes have been created.

        Returns:
            bool: True if all possible child nodes have been created, False otherwise.
        """
        return len(self.children) == len(self.state.get_legal_moves())

    def select_child(
        self,
        exploration_weight: float = math.sqrt(2),  # Theoretical best value
    ) -> Optional[Type[Node]]:
        """
        Select a child node using the UCT (Upper Confidence Bound for Trees) formula.

        Args:
            exploration_weight (float): A hyperparameter that controls
            the balance between exploration and exploitation.

        Returns:
            Node: The selected child node.
        """
        if not self.children:
            return None  # No children to select, return None.

        # Initialise variables for comparison
        best_child = None
        best_score = -float("inf")

        for child in self.children:
            if child.visits == 0:
                # If a child has not been visited at all, we prioritize it for exploration.
                return child

            score = child.value / child.visits + exploration_weight * math.sqrt(
                math.log(self.visits / child.visits)
            )  # UCT formula for child node

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def add_child(self, child_node: Type[Node]):
        """
        Add a child node to this node.

        Args:
            child_node (Node): The child node to add.
        """
        self.children.append(child_node)

    def update(self, result: float):
        """
        Update the visit count and value of this node based on the result of a simulation.

        Args:
            result (float): The result of a simulation
            (e.g., 1.0 for a win, 0.0 for a draw, -1.0 for a loss).
        """
        self.visits += 1
        self.value += result

    def get_best_child(self) -> Type[Node]:
        """
        Get the child node with the highest value (exploitation).

        Returns:
            Node: The best child node.
        """
        return max(self.children, key=lambda child: child.value)

    def get_most_visited_child(self):
        """
        Get the child node with the most visits (exploration).

        Returns:
            Node: The child node with the most visits.
        """
        return max(self.children, key=lambda child: child.visits)

    def get_state(self):
        """
        Get the game state associated with this node.

        Returns:
            Board: The game state.
        """
        return self.state
