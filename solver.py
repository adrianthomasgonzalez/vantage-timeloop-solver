from copy import deepcopy
from collections import deque
from copy import deepcopy

def is_goal(state, _):
    """
    Goal: all dice of the same color are grouped together
    (each non-empty circle contains only one color,
     and no color is split between circles).
    """
    seen = {}
    for idx, circle in enumerate(state):
        if not circle:
            continue
        if len(set(circle)) != 1:
            return False
        color = circle[0]
        if color in seen:
            return False
        seen[color] = idx
    return True



def generate_moves(state, circle_idx):
    n = len(state)
    dice = state[circle_idx]
    if not dice:
        return []

    results = []

    def recurse(pos, remaining, board):
        if not remaining:
            results.append(board)
            return
        die = remaining[0]
        new_board = deepcopy(board)
        new_board[pos].append(die)
        recurse((pos + 1) % n, remaining[1:], new_board)

    # remove all dice from chosen circle
    base_board = deepcopy(state)
    base_board[circle_idx] = []
    recurse((circle_idx + 1) % n, dice, base_board)
    return results


def solve(initial_state, starting_colors=None):
    """
    BFS-based solver: finds up to 5 solutions in 6 or fewer moves.
    Returns a list of solutions (each is a list of (pick_idx, state_before)).
    Solutions are returned shortest-first.
    """
    max_depth = 6
    max_solutions = 5
    visited = set()
    solutions = []

    queue = deque()
    queue.append((initial_state, []))

    while queue and len(solutions) < max_solutions:
        state, path = queue.popleft()
        depth = len(path)

        key = tuple(tuple(c) for c in state)
        if key in visited:
            continue
        visited.add(key)

        # Check for solution
        if is_goal(state, None):
            solutions.append(path)
            continue

        # Stop exploring if we've reached max depth
        if depth >= max_depth:
            continue

        # Explore all possible moves
        for i in range(len(state)):
            if not state[i]:
                continue
            for new_state in generate_moves(state, i):
                queue.append((
                    new_state,
                    path + [(i + 1, deepcopy(state))]
                ))

    return solutions
