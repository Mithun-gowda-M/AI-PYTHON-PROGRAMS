"""Build a delivery tour with the Nearest Neighbor heuristic."""


def nearest_neighbor(
    distances: dict[str, dict[str, int]], locations: list[str], start: str
) -> tuple[list[str], int]:
    if start not in locations or any(location not in distances for location in locations):
        raise ValueError("Start and every location must have a distance row")
    unvisited = set(locations) - {start}
    route, total, current = [start], 0, start
    while unvisited:
        nearest = min(unvisited, key=lambda place: distances[current][place])
        total += distances[current][nearest]
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    total += distances[current][start]
    route.append(start)
    return route, total


def main() -> None:
    locations = ["Depot", "Customer A", "Customer B", "Customer C", "Customer D"]
    distances = {
        "Depot": {"Depot": 0, "Customer A": 10, "Customer B": 15, "Customer C": 20, "Customer D": 12},
        "Customer A": {"Depot": 10, "Customer A": 0, "Customer B": 8, "Customer C": 18, "Customer D": 9},
        "Customer B": {"Depot": 15, "Customer A": 8, "Customer B": 0, "Customer C": 7, "Customer D": 14},
        "Customer C": {"Depot": 20, "Customer A": 18, "Customer B": 7, "Customer C": 0, "Customer D": 6},
        "Customer D": {"Depot": 12, "Customer A": 9, "Customer B": 14, "Customer C": 6, "Customer D": 0},
    }
    route, distance = nearest_neighbor(distances, locations, "Depot")
    print("Heuristic delivery route:", " -> ".join(route))
    print("Total travel distance:", distance, "km")
    print("Note: Nearest Neighbor is a heuristic and does not guarantee a globally optimal tour.")


if __name__ == "__main__":
    main()
