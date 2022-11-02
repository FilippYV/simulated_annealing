import math
import random
import networkx as nx
import matplotlib.pyplot as plt

# import numpy as np

temperature_min = 10  # minimum value of terperature


# x = np.random.uniform(low=0, high=100)  # initiate x
# k = 50  # times of internal circulation
# y = 0  # initiate result
# t = 0  # time


def initializing_variables():
    number_of_vertices = 6
    # number_of_vertices = int(input("Введите количество вершин - "))
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

    temperature_min = 10  # minimum value of terperature
    k_iteration = 0
    k_iteration_max = 2
    mass_all_trail_weight = []
    mass_all_trail = []
    mass_changes = [[0, 0]]
    mass_temperature = [100]

    table_graph = len_weight_write_in_graph(graph)
    zero_trail = trail_calculation()
    mass_all_trail.append(zero_trail)
    length_original_route = calculation_length_zero_level(zero_trail, table_graph)
    mass_all_trail_weight.append(length_original_route[0])
    # print(length_original_route[0], length_original_route[1])
    while mass_temperature[-1] > temperature_min or k_iteration_max > k_iteration:
        print(k_iteration)
        new_level_graph_trail = random_change(length_original_route[1], mass_changes)
        level = calculation_length_next_level(length_original_route[1], table_graph)
        annealing(mass_all_trail_weight, level[0], new_level_graph_trail[0], k_iteration, mass_temperature)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=1)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)


def annealing(mass_all_trail_weight, new_trail, new_level_graph_trail, k_iteration, mass_temperature):
    k_iteration += 1
    print(k_iteration, ' ==================================================')
    # print(mass_all_trail_weight[-1], new_trail)
    delta = new_level_graph_trail[-1] - new_trail
    # print(delta)
    if delta < 0:
        # print(mass_temperature[0] / math.log(1 + k_iteration))
        mass_temperature.append(mass_temperature[0] / math.log(1 + k_iteration))
        mass_all_trail_weight.append(new_level_graph_trail)
        # print(new_level_graph_trail)
    elif delta > 0:
        p = (mass_temperature[-1] * math.e) ** (- new_trail / mass_temperature[0])
        random_p = random.randint(1, mass_temperature[-1])
        if p > random_p:
            print('от 1 до температуры)))))))))))))))))))))_))')
            mass_all_trail_weight.append(new_level_graph_trail)
            print(mass_all_trail_weight)
    print('========================================')




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
    print('S0 =', length_original_route)
    return [length_original_route, trail_old]


def calculation_length_next_level(zero_trail, table_graph):
    print('-----')
    print(zero_trail, table_graph)
    length_route = 0
    trail_old = zero_trail

    for i in range(len(trail_old) - 1):
        for j in range(len(table_graph)):
            # print(trail_old[i], table_graph[j][0], trail_old[i+1], table_graph[j][1])
            if trail_old[i] == table_graph[j][0] and trail_old[i + 1] == table_graph[j][1] or \
                    trail_old[i + 1] == table_graph[j][0] and trail_old[i] == table_graph[j][1]:
                length_route += table_graph[j][2]
                print(table_graph[j][0], table_graph[j][1], table_graph[j][2])
    print('S =', length_route)
    return length_route, trail_old


def random_change(zero_trail, mass_changes):
    count = 0
    trail_change_mass = zero_trail
    mass_to_changes = False
    while mass_to_changes is not True:
        first_number = random.randint(1, 6)
        second_number = random.randint(1, 6)
        if first_number != second_number:
            for i in range(len(mass_changes)):
                print(mass_changes[i][0], first_number, second_number, mass_changes[i][1])
                if mass_changes[i][0] == first_number and second_number == mass_changes[i][1]:
                    count = False
            if count is not False:
                mass_changes.append([first_number, second_number])
                mass_to_changes = True
    print(mass_changes)
    print(trail_change_mass)
    for i in range(len(trail_change_mass)):
        if trail_change_mass[i] == mass_changes[-1][0]:
            trail_change_mass[i] = mass_changes[-1][1]
        elif trail_change_mass[i] == mass_changes[-1][1]:
            trail_change_mass[i] = mass_changes[-1][0]
    print(trail_change_mass)
    return trail_change_mass, mass_changes


# def calculation_annealing():
#     temperature = 100  # initiate temperature
#     temperature_min = 10  # minimum value of terperature
#     # x = np.random.uniform(low=0, high=100)  # initiate x
#     # k = 50  # times of internal circulation
#     # y = 0  # initiate result
#     # t = 0  # time


if __name__ == '__main__':
    graph_construction()
    # plt.show()
