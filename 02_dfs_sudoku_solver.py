"""Solve a 9x9 Sudoku using recursive DFS and backtracking."""


def is_valid(board: list[list[int]], row: int, col: int, value: int) -> bool:
    if value in board[row] or any(board[r][col] == value for r in range(9)):
        return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    return all(
        board[r][c] != value
        for r in range(box_row, box_row + 3)
        for c in range(box_col, box_col + 3)
    )


def solve_sudoku(board: list[list[int]]) -> bool:
    """Solve board in place; zero denotes an empty cell."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for value in range(1, 10):
                    if is_valid(board, row, col, value):
                        board[row][col] = value
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def main() -> None:
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    if solve_sudoku(board):
        print("Solved Sudoku:")
        for row in board:
            print(" ".join(map(str, row)))
    else:
        print("No solution exists.")


if __name__ == "__main__":
    main()
