from enum import Enum
from queue import LifoQueue, PriorityQueue, Queue
from .state import SearchState
from .algorithm import generic_search


def create_queue_bfs(initial_entry: tuple, *_) -> Queue:
    """
    Create a Filo queue for BFS.
    """
    queue = Queue()
    enqueue_node_bfs(queue, [initial_entry])
    return queue


def enqueue_node_bfs(queue: Queue, child_data: list, reverse=False, *_):
    """
    Add items to Filo queue for BFS.
    """
    nodes = []
    for (station, step_cost, parent, line, zones) in child_data:
        cost = step_cost
        if parent:
            cost = cost + parent.cost

        nodes.append(SearchState(station=station, cost=cost, parent=parent, line=line, zones=zones))

    if reverse:
        nodes.reverse()

    for node in nodes:
        queue.put((node.cost, node))


def create_queue_dfs(initial_entry: tuple, *_) -> Queue:
    """
    Create a Lifo queue for DFS.
    """
    queue = LifoQueue()
    enqueue_node_dfs(queue, [initial_entry])
    return queue


def enqueue_node_dfs(queue: LifoQueue, child_data: list, reverse: bool = False, *_):
    """
    Add items to Lifo queue for DFS.
    """
    nodes = []
    for (station, step_cost, parent, line, zones) in child_data:
        cost = step_cost
        if parent:
            cost = cost + parent.cost

        nodes.append(SearchState(station=station, cost=cost, parent=parent, line=line, zones=zones))

    if not reverse:
        nodes.reverse()

    for node in nodes:
        queue.put((node.cost, node))


def create_queue_ucs(initial_entry: tuple, *_) -> Queue:
    """
    Create priority queue for UCS.
    """
    queue = PriorityQueue()
    enqueue_node_ucs(queue, [initial_entry])
    return queue


def enqueue_node_ucs(
    queue: PriorityQueue,
    child_data: list,
    reverse: bool = False,
    line_change_cost: int = 0,
    *_
):
    """
    Add items to priority queue for UCS.
    """
    nodes = []
    for (station, step_cost, parent, line, zones) in child_data:
        cost = step_cost
        if parent:
            cost = cost + parent.cost

        if parent and parent.line and parent.line != line:
            cost = cost + line_change_cost

        nodes.append(SearchState(station=station, cost=cost, parent=parent, line=line, zones=zones))

    if not reverse:
        nodes.reverse()

    for node in nodes:
        queue.put((node.cost, node))


def create_queue_best_first(initial_entry: tuple, goal_zones: set) -> Queue:
    """
    Create queue for best-first search.
    """
    queue = Queue()
    enqueue_node_best_first(queue, [initial_entry], goal_zones=goal_zones)
    return queue


def best_first_heuristic(current_zones: set, goal_zones: set) -> int:
    """
    Heuristic function for best-first search.
        Parameters:
            current_zones (set): primary and secondary zones of current station
            goal_zones (set): primary and secondary zones of goal station

        Returns:
            (int): Heuristic estimating number of minutes to the goal
    """

    # map each zone to an integer to calculate the number of zones from
    # a station to the goal
    zone_positions = {
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        'a': 7, 'b': 8, 'c': 9, 'd': 10
    }

    # calculate the least difference between zones for the two stations
    current_zone_positions = {zone_positions[current_zone] for current_zone in current_zones}
    goal_zone_positions = {zone_positions[goal_zone] for goal_zone in goal_zones}
    min_zone_difference = min(
        abs(min(goal_zone_positions) - max(current_zone_positions)),
        abs(min(current_zone_positions) - max(goal_zone_positions))
    )

    # add a cost of 10 minutes per zone between the two stations
    return 10 * min_zone_difference


def enqueue_node_best_first(
    queue: Queue,
    child_data: list,
    reverse=False,
    line_change_cost: int = 0,
    goal_zones: set = None
):
    """
    Function to enqueue items for best-first search.
    """
    nodes_with_heuristic = []
    for (station, step_cost, parent, line, zones) in child_data:
        cost = step_cost
        if parent:
            cost = cost + parent.cost

        nodes_with_heuristic.append((
            SearchState(station=station, cost=cost, parent=parent, line=line, zones=zones),
            best_first_heuristic(zones, goal_zones)
        ))

    if len(nodes_with_heuristic) > 0:
        pass
    else:
        raise Exception('No more nodes to explore; algorithm failed')

    sorted_nodes = sorted(nodes_with_heuristic, key=lambda node: node[1], reverse=False)
    agenda_length = 2
    for i in range(min(agenda_length, len(nodes_with_heuristic))):
        node, _ = sorted_nodes[i]
        queue.put((node.cost, node))


class Algorithm(Enum):
    """
    Enum which maps the name of a search algorithm to one of the implementations above.
    """
    BreadthFirst = create_queue_bfs, enqueue_node_bfs
    DepthFirst = create_queue_dfs, enqueue_node_dfs
    UniformCost = create_queue_ucs, enqueue_node_ucs
    BestFirst = create_queue_best_first, enqueue_node_best_first

    def __init__(self, create_queue_fn, enqueue_node_fn):
        self.create_queue_fn = create_queue_fn
        self.enqueue_node_fn = enqueue_node_fn

    @staticmethod
    def from_string(label):
        if label == 'BreadthFirst':
            return Algorithm.BreadthFirst
        elif label == 'DepthFirst':
            return Algorithm.DepthFirst
        elif label == 'UniformCost':
            return Algorithm.UniformCost
        elif label == 'BestFirst':
            return Algorithm.BestFirst
        else:
            raise NotImplementedError


def variant_search(
    start: str,
    goal: str,
    algorithm: Algorithm,
    reverse: bool = False,
    line_change_cost: int = 0
) -> tuple:
    """
    Search algorithm that allows selection of parameters:
      - the 'algorithm' parameter can be changed to select the search algorithm used
      - the 'line_change_cost' parameter can be changed to set a cost in minutes of changing lines

        Parameters:
            start            (str):       start station for search
            goal             (str):       goal station for search
            algorithm        (Algorithm): enum selection of the algorithm
            reverse          (bool):      reverse order of nodes before adding to the queue
            line_change_cost (int):       line change cost in minutes

        Returns:
            (tuple[list[str], int, int]): Path of station names from the start to the goal, the cost, in minutes,
                of the path and the total number of nodes explored before the goal is reached
    """
    return generic_search(start, goal, algorithm.create_queue_fn, algorithm.enqueue_node_fn, reverse, line_change_cost)
