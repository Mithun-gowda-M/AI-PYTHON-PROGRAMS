"""Place eight sensors without conflicts using backtracking."""

N = 8


def solve_n_queens(size: int = N) -> list[int] | None:
    """Return column positions (one per row) for one valid board."""
    positions = [-1] * size

    def place(row: int) -> bool:
        if row == size:
            return True
        for col in range(size):
            if all(
                positions[previous] != col
                and abs(positions[previous] - col) != row - previous
                for previous in range(row)
            ):
                positions[row] = col
                if place(row + 1):
                    return True
                positions[row] = -1
        return False

    return positions if place(0) else None


def main() -> None:
    solution = solve_n_queens()
    if solution is None:
        print("No solution exists.")
        return
    print("Conflict-free sensor placement (S = sensor):")
    for queen_col in solution:
        print(" ".join("S" if col == queen_col else "." for col in range(N)))


if __name__ == "__main__":
    main()
