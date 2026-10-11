"""Find a minimum-hop delivery route with breadth-first search."""

from collections import deque


def bfs_shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """Return a shortest path in an unweighted graph, or None if unreachable."""
    if start not in graph or goal not in graph:
        raise ValueError("Start and goal must be nodes in the graph")
    queue = deque([start])
    parent: dict[str, str | None] = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]  # type: ignore[assignment]
            return list(reversed(path))
        for neighbor in graph[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    return None


def main() -> None:
    graph = {
        "A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
        "D": ["B", "C", "G"], "E": ["C", "G"], "G": ["D", "E"],
    }
    path = bfs_shortest_path(graph, "A", "G")
    if path is None:
        print("No route exists.")
    else:
        print("Shortest path:", " -> ".join(path))
        print("Minimum number of roads:", len(path) - 1)


if __name__ == "__main__":
    main()
