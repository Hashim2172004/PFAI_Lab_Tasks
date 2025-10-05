from functools import lru_cache

def count_nqueens(n: int) -> int:
    """Return the number of N-Queens solutions using DP on bitmasks."""
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def dp(cols: int, diag1: int, diag2: int) -> int:
       
        if cols == full:  # all rows placed
            return 1
        free = ~(cols | diag1 | diag2) & full
        total = 0
        while free:
            bit = free & -free          # pick lowest free column bit
            free ^= bit
            total += dp(cols | bit,
                        (diag1 | bit) << 1 & full,
                        (diag2 | bit) >> 1)
        return total

    return dp(0, 0, 0)

def generate_solutions(n: int, limit: int | None = None):
    """
    Yield boards as list[str] using bitmask DFS guided by the same state.
    Set limit to cap how many solutions to produce.
    """
    full = (1 << n) - 1
    board = [-1] * n  # board[row] = col index
    out = 0

    def dfs(row: int, cols: int, diag1: int, diag2: int):
        nonlocal out
        if limit is not None and out >= limit:
            return
        if row == n:
            # build visual board
            yield ["".join("Q" if c == board[r] else "." for c in range(n)) for r in range(n)]
            out += 1
            return
        free = ~(cols | diag1 | diag2) & full
        while free:
            bit = free & -free
            free ^= bit
            col = bit.bit_length() - 1
            board[row] = col
            yield from dfs(row + 1,
                           cols | bit,
                           (diag1 | bit) << 1 & full,
                           (diag2 | bit) >> 1)
            board[row] = -1

    yield from dfs(0, 0, 0, 0)

if __name__ == "__main__":
    n = 8
    print(f"Total solutions for N={n}: {count_nqueens(n)}")

    # Show the first 2 solutions
    for idx, sol in enumerate(generate_solutions(n, limit=2), 1):
        print(f"\nSolution {idx}:")
        for row in sol:
            print(row)
