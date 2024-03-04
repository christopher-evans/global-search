from typing import Callable
from .state import SearchState
from import_underground_data import station_dict, zone_dict


def expand_children(node: SearchState) -> list:
    """
    Utility function which fetches the list of child nodes, visited or not, of a given node from a dictionary.
        Parameters:
            node (SearchState): node state which child nodes will be returned.

        Returns:
            (list[tuple[str, int, str]]): All connected nodes, of the node provided
    """
    if node.station not in station_dict:
        # something has gone wrong -- trying to expand unknown node
        raise ValueError(f'Invalid station {node.station} not found in station data')

    # filter out child nodes not found in the list of already explored nodes
    return station_dict[node.station]


def filter_child_data(
    child_data: list,
    current_node: SearchState,
    explored_nodes: dict
) -> list:
    """
    Utility function to filter child nodes which have not already been visited along the current line.

        Parameters:
            child_data     (list[tuple[str, int, str]]): child nodes to be tested
            current_node   (SearchState):                current node
            explored_nodes (dict[str, int]):             a dictionary of previously explored nodes together with
                                                         minimum path costs to the nodes from the start

        Returns:
            (list[tuple[str, int, str, str, set]]): Filtered list of child nodes
    """
    enriched_data = []
    for (station, cost, line) in child_data:
        if (station not in explored_nodes) or (line not in explored_nodes[station]):
            enriched_data.append((station, cost, current_node, line, zone_dict[station]))

    return enriched_data


def generic_search(
    start: str,
    goal: str,
    create_queue_fn: Callable,
    enqueue_node_fn: Callable,
    reverse: bool = False,
    line_change_cost: int = 0
) -> tuple:
    """
    Generic search algorithm: given a function 'enqueue_node_fn' to add nodes to a queue object, this function
    implements a search algorithm using this queue to fetch the next node to explore.

        Parameters:
            start            (str):      start station for search
            goal             (str):      goal station for search
            create_queue_fn  (Callable): function to initialize the queue
            enqueue_node_fn  (Callable): function to enqueue a list of nodes
            reverse          (bool):     reverse order of nodes before adding to the queue
            line_change_cost (bool):     cost of changing from one line to another

        Returns:
            (tuple[list[str], int, int]): Path of station names from the start to the goal, the cost, in minutes,
                of the path and the total number of nodes explored before the goal is reached
    """
    if start == goal:
        # already at goal, nothing to do
        return [], 0, 0

    explored_nodes = dict()
    queue = create_queue_fn((start, 0, None, None, zone_dict[start]), zone_dict[goal])

    while not queue.empty():
        # fetch next node from the queue
        _, current_node = queue.get()

        # add to explored nodes, if not already present
        # (may already be present if we visited via a different line)
        if current_node.station not in explored_nodes:
            explored_nodes[current_node.station] = [current_node.line]
        elif current_node.line not in explored_nodes[current_node.station]:
            explored_nodes[current_node.station].append(current_node.line)

        # if we are at the goal, return the path and costs
        if current_node.station == goal:
            return current_node.to_path(), current_node.cost, len(explored_nodes)

        # expand child nodes and add these to the queue
        child_data = expand_children(current_node)
        non_visited_child_data = filter_child_data(
            child_data,
            current_node,
            explored_nodes
        )

        enqueue_node_fn(queue, non_visited_child_data, reverse, line_change_cost, zone_dict[goal])

    # no path from start to goal, raise an error
    raise ValueError(f'Unable to find path from start [{start}] to goal [{goal}]')
