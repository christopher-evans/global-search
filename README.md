
# Requirements

Code has been tested with Python 3.7 and 3.11.  A few libraries are needed for common operations:
* Pandas to load data from CSV file
* Numpy to calculate standard deviation
* Argparse to parse command line arguments and generate help text

```commandline
pip install numpy pandas argparse
```

The data file `tubedata.csv` is provided in the root directory so there is no need to copy a file
to run the code.


# Agenda-based search

To run a search use the command

```commandline
python search.py "Start Station" "Goal Station"
```

Command line flags can be used to select an algorithm, add a line change cost and
reverse the order nodes are explored.  For full documentation use:
```commandline
python search.py -h
```


# Genetic algorithm

To run a search use the command

```commandline
python genetic.py "username"
```

Command line flags are available to set the population size, mating pool size, mutation probability,
cross over probability and maximum number of generations.  For full documentation run:
```commandline
python genetic.py -h
```


Functions `run_multiple_iterations` and `run_hyperparameter_test` are available in the file
`genetic.py` used to calculate average and standard deviation of the number of generations for
multiple runs and multiple parameters.

These are not available from the command line, but can be called manually, for example calls could
be placed in the `if __name__ == '__main__':` block at the bottom of `genetic.py`.