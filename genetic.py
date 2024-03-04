from password_fitness import get_password, get_normalised_fitness
from genetic.algorithm import genetic_search
import numpy as np
from argparse import ArgumentParser


def run_genetic_algorithm(
    student_password: str,
    population_size: int = 100,
    mating_pool_size: int = 50,
    mutation_probability: float = 0.2,
    cross_over_probability: float = 0.8,
    max_number_of_generations: int = 100,
    print_output: bool = False
):
    """
    Genetic algorithm implementation for question 3.1
    """

    # wrap fitness function for this password in lambda
    fitness_function = lambda pool: get_normalised_fitness(pool, student_password)

    # Example of how to get fitness values for a list of candidates
    top_result, pool, fitness_scores, number_of_generations = genetic_search(
        fitness_function,
        len(student_password),
        population_size,
        mating_pool_size,
        mutation_probability,
        cross_over_probability,
        max_number_of_generations
    )

    # display results
    if print_output:
        print('Running generic algorithm...')
        print(f'Population size: {population_size}, mating pool size: {mating_pool_size}')
        print(f'Max number of generations: {max_number_of_generations}')
        print(f'Cross over probability: {cross_over_probability}')
        print(f'Mutation probability: {mutation_probability}')
        print('Student password was: ', student_password)
        print()
        if top_result:
            print('Password with perfect score: ', top_result)
        else:
            print('No password found with perfect score found')
        print('Number of generations to result: ', number_of_generations)

        print('Top five results:')
        for result in pool[:5]:
            print(f'"{result}" [score: {fitness_scores[result]}]')

    return top_result, pool, fitness_scores, number_of_generations


def run_multiple_iterations(number_of_iterations=10):
    """
    Run multiple iterations of genetic algorithm for question 3.3
    """

    student_password = get_password('ec23050')

    population_size = 200
    max_number_of_generations = 100
    mating_pool_size = 100
    mutation_probability = 0.1
    cross_over_probability = 0.8

    list_of_generations = []
    for i in range(number_of_iterations):
        top_result, pool, fitness_scores, number_of_generations = run_genetic_algorithm(
            student_password,
            population_size,
            mating_pool_size,
            mutation_probability,
            cross_over_probability,
            max_number_of_generations
        )
        list_of_generations.append(number_of_generations)

    average = np.average(np.array(list_of_generations))
    standard_deviation = np.std(np.array(list_of_generations))
    print(f'Number of iterations: {number_of_iterations}')
    print(f'Values: {list_of_generations}')
    print(f'Average: {average}')
    print(f'Standard deviation: {standard_deviation}')

    return average, standard_deviation


def run_hyperparameter_test():
    """
    Test genetic algorithm with multiple hyperparameters for question 3.4
    """

    student_password = get_password('ec23050')

    population_size = 200
    max_number_of_generations = 400
    mating_pool_size = 100
    mutation_probabilities = [0.1]
    cross_over_probabilities = [0.4, 0.6, 0.8, 1]

    iterations_per_experiment = 100
    results = []
    for cross_over_probability in cross_over_probabilities:
        for mutation_probability in mutation_probabilities:
            list_of_generations = []
            for i in range(iterations_per_experiment):
                top_result, pool, fitness_scores, number_of_generations = run_genetic_algorithm(
                    student_password,
                    population_size,
                    mating_pool_size,
                    mutation_probability,
                    cross_over_probability,
                    max_number_of_generations
                )
                list_of_generations.append(number_of_generations)

            average = np.average(np.array(list_of_generations))
            standard_deviation = np.std(np.array(list_of_generations))
            results.append((cross_over_probability, mutation_probability, average, standard_deviation))
            print('Result added...')

    for (cross_over_probability, mutation_probability, average, standard_deviation) in results:
        print(f'Cross over probability: {cross_over_probability}')
        print(f'Mutation probability: {mutation_probability}')
        print(f'Average: {average}')
        print(f'Standard deviation: {standard_deviation}')
        print()


def run_command_line():
    parser = ArgumentParser(
        prog='search.py',
        description='Search station data provided in a file with various algorithms'
    )
    parser.add_argument('username', help='EECS username')
    parser.add_argument('-p', '--population_size', default='200', help='Population size')
    parser.add_argument('-m', '--mating_pool_size', default='100', help='Mating pool size')
    parser.add_argument('-a', '--mutation_probability', default='0.1', help='Mutation probability')
    parser.add_argument('-c', '--cross_over_probability', default='0.8', help='Cross over probability')
    parser.add_argument('-g', '--max_no_generations', default='100', help='Max number of generations')
    args = parser.parse_args()

    username = args.username
    population_size = int(args.population_size)
    mating_pool_size = int(args.mating_pool_size)
    mutation_probability = float(args.mutation_probability)
    cross_over_probability = float(args.cross_over_probability)
    max_number_of_generations = int(args.max_no_generations)

    run_genetic_algorithm(
        get_password(username),
        population_size,
        mating_pool_size,
        mutation_probability,
        cross_over_probability,
        max_number_of_generations,
        True
    )


if __name__ == '__main__':
    try:
        run_command_line()
    except Exception as error:
        print(f'Unexpected error: [{error}]')
