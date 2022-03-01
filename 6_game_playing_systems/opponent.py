from mctspy.games.examples.tictactoe import TicTacToeGameState, TicTacToeMove
import random
import copy
from typing import List
from abc import ABC, abstractmethod


class Agent(ABC):
    """
    All agents need to implement policy method
    """

    @abstractmethod
    def policy():
        pass


class RandomAgent(Agent):
    def policy(self, state: TicTacToeGameState) -> TicTacToeMove:
        actions = state.get_legal_actions()
        return random.choice(actions)


class HeuristicAgent(Agent):
    def __init__(self, board_size: int):
        self.board_size = board_size

    def policy(self, state: TicTacToeGameState) -> TicTacToeMove:
        def _filter_corner(move: TicTacToeMove) -> bool:
            if move.x_coordinate == 0 or move.x_coordinate == -1:
                return True
            elif move.y_coordinate == 0 or move.y_coordinate == -1:
                return True
            return False

        def _filter_middle(move: TicTacToeMove) -> bool:
            if move.x_coordinate == self.board_size / 2:
                return True
            elif move.y_coordinate == self.board_size / 2:
                return True
            return False

        def _filter_winning_moves(
            state: TicTacToeGameState, actions: List[TicTacToeMove]
        ) -> List[TicTacToeMove]:
            winning_moves = []
            for a in actions:
                tmp_state = copy.copy(state)
                tmp_state.move(a)
                if tmp_state.is_game_over():
                    winning_moves.append(a)
            return winning_moves

        actions = state.get_legal_actions()

        # check for winning move
        winning_moves = _filter_winning_moves(state, actions)
        if winning_moves:
            return random.choice(winning_moves)

        # prefer moves in corners
        corner_moves = list(filter(_filter_corner, actions))
        if corner_moves:
            return random.choice(corner_moves)

        # prefer moves in the middle
        middle_moves = list(filter(_filter_middle, actions))
        if middle_moves:
            return random.choice(middle_moves)

        # otherwise random
        return random.choice(actions)


class SelfPlayAgent(Agent):
    def policy():
        pass
