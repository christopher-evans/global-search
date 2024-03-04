from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class SearchState:
    """
    A class used to represent state in a search algorithm. The @dataclass annotation
    is used to auto-generate __init__ and __repr__ methods.

    The 'order' annotation is set to true to auto-generate comparison methods for this
    class to enable use with the python PriorityQueue implementation.  Two SearchState
    objects are compared by priority only; objects with equal priority may be retrieved
    in any order.

    Attributes:
        station : str
            Name of the station
        cost : int
            Cost of reaching this station from the start station
        line : str
            Line taken from the parent station to this station
        parent : SearchState
            The previous station in the steps to reach this station from
            the start state
        zones : set[str]
            Primary and secondary zones for the station

    Methods:
        to_path():
            Convert the node to a path by iterating through its parents
    """

    station: str = field(compare=False)
    cost: int
    parent: Any = field(compare=False)
    line: str = field(compare=False)
    zones: set = field(compare=False)

    def to_path(self):
        """
        Convert the node to a path by iterating recursively through the parent property.

        Returns:
            list[str]: List of station names for each stop from the start to the destination
        """
        path = [f'{self.station} ({self.line})']
        current_node = self

        while current_node.parent:
            current_node = current_node.parent
            path.insert(0, f'{current_node.station} ({current_node.line})')

        return path
