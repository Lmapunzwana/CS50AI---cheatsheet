import csv
import sys

from util import Node, QueueFrontier

# Public globals expected by check50 tests
# names: maps lowercase names -> set of person_ids
names = {}

# people: maps person_id -> {"name", "birth", "movies": set(movie_id)}
people = {}

# movies: maps movie_id -> {"title", "year", "stars": set(person_id)}
movies = {}


def load_data(directory):
    """
    Load CSV data from `directory` into the global dicts:
    names, people, movies.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["id"]
            pname = row["name"]
            people[pid] = {
                "name": pname,
                "birth": row["birth"],
                "movies": set()
            }
            key = pname.lower()
            if key not in names:
                names[key] = {pid}
            else:
                names[key].add(pid)

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row["id"]
            movies[mid] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars (relationships)
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["person_id"]
            mid = row["movie_id"]
            # Some rows may reference missing person/movie; ignore those.
            try:
                people[pid]["movies"].add(mid)
                movies[mid]["stars"].add(pid)
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        # Prepend source sentinel to walk pairs easily
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Return the shortest list of (movie_id, person_id) pairs
    that connect source to target. If no path, return None.
    Uses Breadth-First Search (BFS).
    """
    # Initialize root node and frontier for BFS
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    while True:
        if frontier.empty():
            return None

        node = frontier.remove()

        # If we've reached the target, unwind and return path
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add(node.state)

        # Expand neighbors (movie_id, person_id) pairs
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                # goal test here short-circuits sooner
                if child.state == target:
                    path = []
                    while child.parent is not None:
                        path.append((child.action, child.state))
                        child = child.parent
                    path.reverse()
                    return path
                frontier.add(child)


def person_id_for_name(name):
    """
    Resolve a person's name to their person_id.
    If multiple people have the same name, prompt to disambiguate.
    Returns the chosen person_id (string) or None if not found.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            pname = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {pname}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Return (movie_id, person_id) pairs for people who starred
    with the given person.
    """
    neighbor_set = set()
    for movie_id in people[person_id]["movies"]:
        for co_star in movies[movie_id]["stars"]:
            neighbor_set.add((movie_id, co_star))
    return neighbor_set


if __name__ == "__main__":
    main()
