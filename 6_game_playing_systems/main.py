import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode as TreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.tictactoe import TicTacToeGameState, TicTacToeMove
from opponent import RandomAgent, HeuristicAgent
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
    else:
        raise ValueError("Invalid opponent policy")

    while not done:
        # pick action for player whos turn it is

        # player
        if next_to_move == 1:
            root = TreeSearchNode(state=state)
            mcts = MonteCarloTreeSearch(root)
            action = mcts.best_action(10000)
            move = pick_move(state, action, next_to_move)
        # opponent
        elif next_to_move == -1:
            move = opponent.policy(state)
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


def pick_move(
    cur_state: TicTacToeGameState, best_action: TreeSearchNode, next_to_move: int
) -> TicTacToeMove:
    cur_board = cur_state.board
    best_board = best_action.state.board
    diff_board = best_board - cur_board
    x, y = np.where(diff_board == next_to_move)
    return TicTacToeMove(x[0], y[0], next_to_move)


size = 3
state = np.zeros((size, size))
next_to_move = -1
games = 10

initial_board_state = TicTacToeGameState(state=state, next_to_move=next_to_move)

start_time = time.perf_counter()
results = [
    play(
        initial_board_state, next_to_move, i, opponent_policy="heuristic", verbose=False
    )
    for i in range(games)
]
end_time = time.perf_counter()

won_cnt = results.count(1)
print(
    f"Player won {won_cnt}/{games} games. {(won_cnt/games)*100}% in {round(end_time - start_time, 2)}sec"
)
