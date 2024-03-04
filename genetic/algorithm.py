import string
import random
from typing import Callable

OPTIONS = string.digits + string.ascii_uppercase + "_"


def create_initial_pool(population_size: int, password_length: int) -> list:
    """
    Create an initial pool of passwords with a given size and length.
        Parameters:
            population_size (int): pool size
            password_length (int): length of passwords in the pool

        Returns:
            (list[tuple[str, int, str]]): All connected nodes, of the node provided
    """
    pool = []
    for index in range(population_size):
        individual = ''.join(random.choices(OPTIONS, k=password_length))
        pool.append(individual)

    return pool


def mutate_password(password: str, mutation_probability: float) -> str:
    """
    Mutate characters in a password at random with a given probability.
        Parameters:
            password (str): password
            mutation_probability (float): probability of mutating each character

        Returns:
            (str): Mutated password
    """
    mutation = list(password)
    for index in range(len(mutation)):
        if random.uniform(0, 1) < mutation_probability:
            mutation[index] = random.choice(OPTIONS)

    return ''.join(mutation)


def mutate_pool(pool: list, mutation_probability: float) -> list:
    """
    Mutate each password in a pool.
        Parameters:
            pool (list): list of passwords
            mutation_probability (float): probability of mutating each character in each password

        Returns:
            (list): Mutated pool
    """
    for index, individual in enumerate(pool):
        pool[index] = mutate_password(individual, mutation_probability)

    return pool


def cross_over_passwords(first: str, second: str) -> str:
    """
    Combine two passwords by selecting a random character n from 1 to len(password)-1 and combining
    the first n characters of one password with the last n characters of the second.
        Parameters:
            first (str): first password
            second (str): second password

        Returns:
            (str): Combined password
    """
    cross_over_point = random.randrange(1, len(first) - 1)

    return first[:cross_over_point] + second[cross_over_point:]


def cross_over_pool(pool: list, cross_over_probability: float):
    """
    Cross over every password in a pool with another randomly selected password with a given probability.
        Parameters:
            pool (list): pool of passwords
            cross_over_probability (float): probability each password is crossed-over

        Returns:
            (list): List of children from the password in the pool
    """
    if len(pool) < 2:
        raise ValueError('Cross over pool size must be at least 2')

    offspring = []
    for index, individual in enumerate(pool):
        if random.uniform(0, 1) > cross_over_probability:
            continue

        # select a second individual from the pool for cross over
        mate_index = index
        while mate_index == index:
            mate_index = random.randrange(0, len(pool))

        offspring.append(cross_over_passwords(individual, pool[mate_index]))

    return offspring


def genetic_search(
    fitness_function: Callable,
    password_length: int,
    population_size: int = 100,
    mating_pool_size: int = 50,
    mutation_probability: float = 0.1,
    cross_over_probability: float = 0.8,
    max_number_of_generations: int = 100
) -> tuple:
    """
    Apply a genetic algorithm to search for a password of a given length.
        Parameters:
            fitness_function (Callable): Function to call to determine fitness of an individual
            password_length (int): length of the password
            population_size (int): size of pool of individuals used for the search
            mating_pool_size (int): subset of the pool to use for crossing-over individuals
            mutation_probability (float): probability of mutating each character in the offspring of the mating pool
            cross_over_probability (float): probability of crossing over one individual in the mating pool
            max_number_of_generations (int): maximum number of generations to run the algorithm before returning
                                             the best result

        Returns:
            (str, list, dict, int):
                most fit individual found,
                current pool of passwords,
                fitness scores for each individual in the pool,
                total number of generations the algorithm ran for
    """
    fitness_scores = dict()
    pool = create_initial_pool(population_size, password_length)
    for generation_counter in range(max_number_of_generations):
        # select most fit individuals for cross over
        fitness_scores = fitness_function(pool)
        mating_pool = sorted(pool, key=lambda individual: fitness_scores[individual], reverse=True)[:mating_pool_size]

        # cross over these individuals
        offspring = cross_over_pool(mating_pool, cross_over_probability)
        offspring = mutate_pool(offspring, mutation_probability=mutation_probability)

        # merge the most fit individuals with the offspring, keeping
        # the most fit individuals from this pool
        all_individuals = [*mating_pool, *offspring]
        fitness_scores = fitness_function(all_individuals)

        # create new pool from parents and offspring
        pool = sorted(
            all_individuals,
            key=lambda individual: fitness_scores[individual],
            reverse=True
        )[:population_size]
        most_fit_individual = pool[0]
        if fitness_scores[most_fit_individual] >= 1:
            return most_fit_individual, pool, fitness_scores, generation_counter

    return None, pool, fitness_scores, max_number_of_generations
