import random
from copy import deepcopy
from solver import solve, is_goal
import sys
sys.setrecursionlimit(500000)


colors = ['G','R','Y','B','O','P']

def generate_solvable_board():
    """
    Generate a guaranteed solvable board for testing.
    Randomly assign 2 dice of each color to a single circle.
    """
    dice = colors * 2
    random.shuffle(dice)
    board = [dice[i:i+2] for i in range(0, 12, 2)]
    return board

def validate_solution(board, solution):
    """
    Validate that the solution is legal:
    - Picks up dice from correct circle
    - Drops dice in order
    - Board updates correctly
    """
    n = len(board)
    state = deepcopy(board)
    
    for step_num, (pick_idx, state_before) in enumerate(solution, 1):
        # Check that state_before matches current state
        if state_before != state:
            print(f"❌ Step {step_num}: state_before mismatch!")
            print("Expected:", state)
            print("Got:", state_before)
            return False

        dice_to_move = state[pick_idx-1]
        if not dice_to_move:
            print(f"❌ Step {step_num}: picked up from empty circle {pick_idx}")
            return False

        state[pick_idx-1] = []

        # Simulate dropping dice clockwise
        pos = pick_idx % n
        for die in dice_to_move:
            state[pos].append(die)
            pos = (pos + 1) % n

    # Final check: board solved?
    if not is_goal(state, set(colors)):
        print("❌ Final state not solved!")
        print(state)
        return False

    print("✅ Solution valid!")
    return True

def run_tests(num_tests=5):
    for i in range(num_tests):
        board = generate_solvable_board()
        print(f"\nTest {i+1} board: {board}")
        solution = solve(board, set(colors))
        if solution:
            print("Solver returned a solution. Validating...")
            validate_solution(board, solution)
        else:
            print("❌ Solver returned unsolvable on guaranteed solvable board!")

# Run 5 test cases
run_tests()
