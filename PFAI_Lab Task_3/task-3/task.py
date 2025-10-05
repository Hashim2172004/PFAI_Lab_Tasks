# Water Jug Problem using Depth-First Search (DFS)
# Rules:
# R1: Fill A        R2: Fill B
# R3: Empty A       R4: Empty B
# R5: Pour A -> B   R6: Pour B -> A

from collections import deque

def neighbors(state, capA, capB):
    a, b = state
    moves = []

    # R1: Fill A
    if a < capA:
        moves.append(((capA, b), "R1: Fill A"))

    # R2: Fill B
    if b < capB:
        moves.append(((a, capB), "R2: Fill B"))

    # R3: Empty A
    if a > 0:
        moves.append(((0, b), "R3: Empty A"))

    # R4: Empty B
    if b > 0:
        moves.append(((a, 0), "R4: Empty B"))

    # R5: Pour A -> B
    if a > 0 and b < capB:
        pour = min(a, capB - b)
        moves.append(((a - pour, b + pour), f"R5: Pour A→B ({pour})"))

    # R6: Pour B -> A
    if b > 0 and a < capA:
        pour = min(b, capA - a)
        moves.append(((a + pour, b - pour), f"R6: Pour B→A ({pour})"))

    return moves

def water_jug_dfs(capA, capB, goal):
    """
    Returns the sequence of (action, resulting_state) from (0,0) to any state where
    jug A == goal or jug B == goal, using DFS. If not found, returns None.
    """
    start = (0, 0)
    stack = [(start, [])]  # (state, path_of_actions)
    visited = set([start])

    while stack:
        state, path = stack.pop()
        a, b = state

        # goal condition: either jug has the target amount
        if a == goal or b == goal:
            return path + [("Goal reached", state)]

        for next_state, action in neighbors(state, capA, capB):
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [(action, next_state)]))

    return None

def print_solution(path):
    if not path:
        print("No solution found.")
        return
    print("Solution (DFS):")
    for step_num, (action, (a, b)) in enumerate(path, 1):
        print(f"Step {step_num:02d} | {action:20s} -> State: (A={a}, B={b})")

if __name__ == "__main__":
    # Example: capacities A=4, B=3, goal=2 (classic problem)
    capA, capB, goal = 4, 3, 2
    path = water_jug_dfs(capA, capB, goal)
    print_solution(path)
