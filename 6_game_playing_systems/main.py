# import mctspy manually
import sys

sys.path.append("./mctspy")

import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode as TreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.tictactoe import TicTacToeGameState
from opponent import RandomAgent, HeuristicAgent, pick_move, SelfPlayAgent, HumanAgent
import copy
import time


def play(
    init_state: TicTacToeGameState,
    next_to_move: int,
    game_idx: int,
    opponent_policy: str = "random",
    verbose: bool = False,
):
    print(f"Playing game {game_idx+1}")
    state = copy.copy(init_state)
    done = False
    time_step = 0

    # pick opponent_policy
    if opponent_policy == "random":
        opponent = RandomAgent()
    elif opponent_policy == "heuristic":
        opponent = HeuristicAgent(init_state.board_size)
    elif opponent_policy == "selfplay":
        opponent = SelfPlayAgent()
    elif opponent_policy == "human":
        opponent = HumanAgent()
    else:
        raise ValueError("Invalid opponent policy")

    while not done:
        # pick action for player whos turn it is
        root = TreeSearchNode(state=state)
        mcts = MonteCarloTreeSearch(root)

        # player
        if next_to_move == 1:
            action = mcts.best_action(10000)
            move = pick_move(state, action, next_to_move)
        # opponent
        elif next_to_move == -1:
            move = (
                opponent.policy(mcts, state)
                if opponent_policy == "selfplay"
                else opponent.policy(state)
            )
        else:
            raise ValueError("Invalid move turn")

        state = state.move(move)
        done = state.is_game_over()
        next_to_move = -next_to_move  # negate to change turn
        time_step += 1

    result = state.game_result

    # game is finished
    if verbose:
        print(state.board)
        print(f"{time_step + 1} rounds.")

        if result == 1:
            print("Player wins!")
        elif result == -1:
            print("Opponent wins!")
        else:
            print("Draw!")

    return result


"""
Game settings
"""
size = 3  # size of board
state = np.zeros((size, size))
next_to_move = -1  # 1 player starts, -1 opponent starts
games = 10  # number of played games
opponent_policy = "random"  # random, heuristic, selfplay, human

initial_board_state = TicTacToeGameState(state=state, next_to_move=next_to_move)

start_time = time.perf_counter()
results = [
    play(
        initial_board_state,
        next_to_move,
        i,
        opponent_policy=opponent_policy,
        verbose=True,
    )
    for i in range(games)
]
end_time = time.perf_counter()

won_cnt = results.count(1)
draw_cnt = results.count(0)
print(
    f"Player won {won_cnt}/{games} games. {(won_cnt/games)*100}% in {round(end_time - start_time, 2)}sec"
)
print(
    f"Player draw {draw_cnt}/{games} games. {(draw_cnt/games)*100}% in {round(end_time - start_time, 2)}sec"
)
