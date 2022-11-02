import random
import networkx as nx
import matplotlib.pyplot as plt


# import numpy as np


def initializing_variables():
    number_of_vertices = 6
    # number_of_vertices = int(input("Введите количество граней - "))
    return number_of_vertices


def len_calculations():
    number_of_vertices = initializing_variables()
    len_weight = []
    for i in range(1, number_of_vertices + 1):
        for ii in range(i + 1, number_of_vertices + 1):
            len_weight.append([i, ii, random.randint(50, 101)])
    # len_weight = [[1, 2, 52], [1, 3, 73], [1, 4, 87], [1, 5, 66], [1, 6, 89], [2, 3, 60], [2, 4, 59], [2, 5, 54],
    # [2, 6, 90], [3, 4, 100], [3, 5, 79], [3, 6, 79], [4, 5, 58], [4, 6, 93], [5, 6, 69]]
    print(len_weight)
    return len_weight


def len_weight_write_in_graph(graph):
    len_weight = len_calculations()
    for i in range(len(len_weight)):
        graph.add_edge(len_weight[i][0], len_weight[i][1], weight=len_weight[i][2])
    # print(len_weight)
    return len_weight


def trail_calculation():
    number_of_vertices = initializing_variables()
    trail = []
    while len(trail) != number_of_vertices:
        cache = random.randint(1, number_of_vertices)
        if cache not in trail:
            trail.append(cache)
    # trail = [1, 4, 3, 5, 2, 6]
    # print(trail)
    return trail


def graph_construction():
    graph = nx.Graph()

    table_graph = len_weight_write_in_graph(graph)
    zero_trail = trail_calculation()
    length_original_route = calculation_length_zero_level(zero_trail, table_graph)
    mass_changes = [[0, 0]]
    random_change(length_original_route[1], mass_changes)
    level = calculation_length_next_level(length_original_route[0], length_original_route[1])

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=1)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)


def calculation_length_zero_level(zero_trail, table_graph):
    length_original_route = 0
    trail_old = zero_trail
    trail_old.append(trail_old[0])
    for i in range(len(trail_old) - 1):
        for j in range(len(table_graph)):
            # print(trail_old[i], table_graph[j][0], trail_old[i+1], table_graph[j][1])
            if trail_old[i] == table_graph[j][0] and trail_old[i + 1] == table_graph[j][1] or \
                    trail_old[i + 1] == table_graph[j][0] and trail_old[i] == table_graph[j][1]:
                length_original_route += table_graph[j][2]
                print(table_graph[j][0], table_graph[j][1], table_graph[j][2])
    print('S0 =', length_original_route)
    return [length_original_route, trail_old]


def calculation_length_next_level(zero_trail, table_graph):
    length_route = 0
    trail_old = zero_trail
    for i in range(len(trail_old) - 1):
        for j in range(len(table_graph)):
            # print(trail_old[i], table_graph[j][0], trail_old[i+1], table_graph[j][1])
            if trail_old[i] == table_graph[j][0] and trail_old[i + 1] == table_graph[j][1] or \
                    trail_old[i + 1] == table_graph[j][0] and trail_old[i] == table_graph[j][1]:
                length_route += table_graph[j][2]
                print(table_graph[j][0], table_graph[j][1], table_graph[j][2])
    print('S0 =', length_route)
    return length_route, trail_old


def random_change(zero_trail, mass_changes):
    count = 0
    trail_change_mass = zero_trail
    mass_to_changes = []
    while mass_to_changes == 0:
        first_number = random.randint(1, 6)
        second_number = random.randint(1, 6)
        if first_number != second_number:
            for i in range(len(mass_changes)):
                if mass_changes[i][0] != first_number and second_number != mass_changes[i][1]:
                    count += 1


# def calculation_annealing():
#     temperature = 100  # initiate temperature
#     temperature_min = 10  # minimum value of terperature
#     # x = np.random.uniform(low=0, high=100)  # initiate x
#     # k = 50  # times of internal circulation
#     # y = 0  # initiate result
#     # t = 0  # time


if __name__ == '__main__':
    graph_construction()
    plt.show()
