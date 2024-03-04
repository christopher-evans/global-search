from search.variants import variant_search, Algorithm
from argparse import ArgumentParser


def print_output(path: list, cost: int, explored_nodes: int):
    print()
    print('Path cost (minutes):      ', cost)
    print('Number of nodes explored: ', explored_nodes)
    print('Path found:               ', path)


def run_search():
    """
    Parse command line arguments and search based on those values.
    """

    # create argument parser for command line use
    parser = ArgumentParser(
        prog='search.py',
        description='Search station data provided in a file with various algorithms'
    )
    parser.add_argument('start', help='Start station')
    parser.add_argument('goal', help='Goal station')
    parser.add_argument(
        '-a',
        '--algorithm',
        default='BreadthFirst',
        choices=['BreadthFirst', 'DepthFirst', 'UniformCost', 'BestFirst'],
        help='select algorithm'
    )
    parser.add_argument(
        '-l',
        '--line_change_cost',
        default='0',
        help='cost of a line change, in minutes; must be positive or zero'
    )
    parser.add_argument(
        '-r',
        '--reverse',
        action='store_true',
        help='reverse the order of nodes when adding to the queue'
    )
    args = parser.parse_args()

    # parse command line arguments
    start = args.start
    goal = args.goal
    algorithm = Algorithm.from_string(args.algorithm)
    line_change_cost = int(args.line_change_cost)
    reverse = bool(args.reverse)

    # Print search request to user
    print('Performing search...')
    print(f'From [{start}] to [{goal}] using algorithm [{args.algorithm}]')
    if line_change_cost > 0:
        print(f'Line change cost: [{line_change_cost}]')

    # perform search and print results
    try:
        path, cost, explored_nodes = variant_search(start, goal, algorithm, reverse, line_change_cost)
        print_output(path, cost, explored_nodes)
    except ValueError as value_error:
        print(f'Failed to complete search: [{value_error}]')
    except FileNotFoundError as file_not_found_error:
        print(f'Failed to load data: [{file_not_found_error}]')


if __name__ == '__main__':
    try:
        run_search()
    except NotImplementedError as not_implemented_error:
        print(f'Algorithm not known: [{not_implemented_error}]')
    except Exception as error:
        print(f'Unexpected error: [{error}]')
