"""Plan an optimal four-direction warehouse route with A* search."""

import heapq
from itertools import count

Cell = tuple[int, int]


def heuristic(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid: list[list[int]], start: Cell, goal: Cell) -> list[Cell] | None:
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Grid must be a non-empty rectangle")
    rows, cols = len(grid), len(grid[0])
    for r, c in (start, goal):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 1:
            raise ValueError("Start and goal must be free cells inside the grid")

    sequence = count()
    frontier = [(heuristic(start, goal), next(sequence), start)]
    cost = {start: 0}
    parent: dict[Cell, Cell | None] = {start: None}
    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]  # type: ignore[assignment]
            return path[::-1]
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = current[0] + dr, current[1] + dc
            r, c = neighbor
            new_cost = cost[current] + 1
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost + heuristic(neighbor, goal), next(sequence), neighbor))
    return None


def main() -> None:
    warehouse = [
        [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0],
    ]
    start, goal = (0, 0), (5, 5)
    path = a_star(warehouse, start, goal)
    if path is None:
        print("No path exists.")
        return
    print("Optimal path:", path)
    print("Number of movements:", len(path) - 1)
    display = [["#" if cell else "." for cell in row] for row in warehouse]
    for row, col in path:
        display[row][col] = "*"
    display[start[0]][start[1]], display[goal[0]][goal[1]] = "S", "G"
    print("Warehouse (* = path, # = obstacle):")
    for row in display:
        print(" ".join(row))


if __name__ == "__main__":
    main()
