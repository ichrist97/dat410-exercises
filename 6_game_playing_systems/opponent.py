import random
import copy
from typing import List
from abc import ABC, abstractmethod
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode as TreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.tictactoe import TicTacToeGameState, TicTacToeMove
import numpy as np


def pick_move(
    cur_state: TicTacToeGameState, best_action: TreeSearchNode, next_to_move: int
) -> TicTacToeMove:
    """
    Map best node from mcts run a to move in tictactoe
    """
    cur_board = cur_state.board
    best_board = best_action.state.board
    diff_board = best_board - cur_board
    x, y = np.where(diff_board == next_to_move)
    return TicTacToeMove(x[0], y[0], next_to_move)


class Agent(ABC):
    """
    All agents need to implement policy method
    """

    @abstractmethod
    def policy():
        pass


class RandomAgent(Agent):
    """
    Choose moves randomly
    """

    def policy(self, state: TicTacToeGameState) -> TicTacToeMove:
        actions = state.get_legal_actions()
        return random.choice(actions)


class HeuristicAgent(Agent):
    """
    Pick preferable moves by heuristics, otherwise random
    """

    def __init__(self, board_size: int):
        self.board_size = board_size

    def policy(self, state: TicTacToeGameState) -> TicTacToeMove:
        """
        Select action accordinto handpicked heuristics
        """

        def _filter_corner(move: TicTacToeMove) -> bool:
            """
            Look for open corners in board
            """
            if move.x_coordinate == 0 or move.x_coordinate == -1:
                return True
            elif move.y_coordinate == 0 or move.y_coordinate == -1:
                return True
            return False

        def _filter_middle(move: TicTacToeMove) -> bool:
            """
            Look for open middle parts in the board
            """
            if move.x_coordinate == self.board_size / 2:
                return True
            elif move.y_coordinate == self.board_size / 2:
                return True
            return False

        def _filter_winning_moves(
            state: TicTacToeGameState, actions: List[TicTacToeMove]
        ) -> List[TicTacToeMove]:
            """
            Look for a potential winning move
            """
            winning_moves = []
            for a in actions:
                tmp_state = copy.deepcopy(state)
                tmp_state = tmp_state.move(a)
                if tmp_state.is_game_over():
                    winning_moves.append(a)
            return winning_moves

        def _filter_losing_move(state: TicTacToeGameState) -> TicTacToeMove:
            """
            Look for a move that will win the game for oppponent and try to hinder that move
            """
            board = state.board
            # rows
            for idx, row in enumerate(board):
                if np.sum(row) == (state.board_size - 1):
                    y = np.where(row == 0)[0][0]
                    x = idx
                    return TicTacToeMove(x, y, -1)
            # cols
            for idx, col in enumerate(board.T):
                if np.sum(col) == (state.board_size - 1):
                    x = np.where(col == 0)[0][0]
                    y = idx
                    return TicTacToeMove(x, y, -1)
            # top right to bottom left diagonal
            diag = board.diagonal()
            if np.sum(diag) == (state.board_size - 1):
                x = np.where(diag == 0)[0][0]
                return TicTacToeMove(x, x, -1)

            # bottom left to top right diagonal
            diag = np.flipud(board.diagonal())
            if np.sum(diag) == (state.board_size - 1):
                x = np.where(diag == 0)[0][0]
                return TicTacToeMove(x, x, -1)
            return None

        actions = state.get_legal_actions()

        # check for winning move
        winning_moves = _filter_winning_moves(state, actions)
        if winning_moves:
            return random.choice(winning_moves)

        # check for losing move to player
        losing_move = _filter_losing_move(state)
        if losing_move:
            return losing_move

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
    def policy(
        self, mcts: MonteCarloTreeSearch, state: TicTacToeGameState
    ) -> TicTacToeMove:
        """
        Pick best action from monte carlo tree search like agent player
        """
        action = mcts.best_action(10000)
        return pick_move(state, action, -1)


class HumanAgent(Agent):
    def policy(self, state: TicTacToeGameState):
        print("Current board:")
        print(state.board)

        move = input('Type in the coordinates of your move as "x,y":\n> ')
        x, y = move.split(",")[0], move.split(",")[1]
        print("AI decides for the next move...")
        return TicTacToeMove(int(x), int(y), -1)
