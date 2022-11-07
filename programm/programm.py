import math
import random
import networkx as nx
import matplotlib.pyplot as plt

temperature_min = 10  # minimum value of terperature


def initializing_variables():
    number_of_vertices = 6
    # number_of_vertices = int(input("Введите количество вершин - "))
    return number_of_vertices


def len_calculations():
    number_of_vertices = initializing_variables()
    len_weight = []
    # for i in range(1, number_of_vertices + 1):
    #     for j in range(i + 1, number_of_vertices + 1):
    #         len_weight.append([i, j, random.randint(50, 101)])
    len_weight = [[1, 2, 52], [1, 3, 73], [1, 4, 87], [1, 5, 66], [1, 6, 89], [2, 3, 60], [2, 4, 59], [2, 5, 54],
                  [2, 6, 90], [3, 4, 100], [3, 5, 79], [3, 6, 79], [4, 5, 58], [4, 6, 93], [5, 6, 69]]
    # print(len_weight)
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
    minimum_temperature = 10  # minimum value of terperature
    mass_iteration = [1]
    k_iteration_max = 200
    mass_all_trail_weight = []
    mass_all_trail = []
    mass_temperature = [100]

    table_graph = len_weight_write_in_graph(graph)
    zero_trail = trail_calculation()
    mass_all_trail.append(zero_trail)
    length_original_route = calculation_length_zero_level(zero_trail, table_graph)
    mass_all_trail_weight.append(length_original_route[0])
    while mass_temperature[-1] > minimum_temperature and k_iteration_max + 1 > len(mass_iteration):
        print()
        new_level_graph_trail = random_change_road(mass_all_trail, mass_iteration)
        level = calculation_length_next_level(length_original_route[1], table_graph)
        annealing(mass_all_trail_weight, level[0], mass_iteration, mass_temperature)
    print(f'Финальный вариант пути: {mass_all_trail_weight}')

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=1)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)


def annealing(mass_all_trail_weight, new_trail, mass_iteration, mass_temperature):
    mass_iteration.append(mass_iteration[-1] + 1)
    print(f'Старая температура: {mass_temperature[-1]}')
    print(f'OLD S - {mass_all_trail_weight[-1]}')
    print(f'NEW S - {new_trail}')
    delta = new_trail - mass_all_trail_weight[-1]
    print(f'delta = {new_trail}', '-', f'{mass_all_trail_weight[-1]} = {delta}')
    if delta < 0:
        print(f'{delta} < 0')
        print('Расчёт температуры:')
        print(f'{mass_temperature[0]} / {math.log(1 + mass_iteration[-1])}')
        new_temp = round(mass_temperature[0] / math.log(1 + mass_iteration[-1]), 3)
        mass_temperature.append(new_temp)
        print(f'Новая температура - {mass_temperature[-1]}')
        mass_all_trail_weight.append(new_trail)
    elif delta > 0:
        print(f'{delta} > 0')
        # p = 100 * math.e ** (-new_trail/mass_temperature[-1])
        p = (mass_temperature[0] * math.e) ** (- delta / mass_temperature[0])
        random_p = round((random.uniform(1, mass_temperature[-1])), 3)
        print(random_p)
        print(f'{p} =?= {random_p}')
        if p >= random_p:
            print(f'{p} >= {random_p}')
            mass_all_trail_weight.append(new_trail)
            print(mass_all_trail_weight)
        else:
            print(f'{p} < {random_p}')
            print('Не принимаем маршрут!')
            mass_all_trail_weight.append(mass_all_trail_weight[-1])
    print('=' * 100)


def calculation_length_zero_level(zero_trail, table_graph):
    length_original_route = 0
    trail_old = zero_trail
    trail_old.append(trail_old[0])
    for i in range(len(trail_old) - 1):
        for j in range(len(table_graph)):
            if trail_old[i] == table_graph[j][0] and trail_old[i + 1] == table_graph[j][1] or \
                    trail_old[i + 1] == table_graph[j][0] and trail_old[i] == table_graph[j][1]:
                length_original_route += table_graph[j][2]
    return [length_original_route, trail_old]


def calculation_length_next_level(zero_trail, table_graph):
    length_route = 0
    trail_old = zero_trail
    for i in range(len(trail_old) - 1):
        for j in range(len(table_graph)):
            if trail_old[i] == table_graph[j][0] and trail_old[i + 1] == table_graph[j][1] or \
                    trail_old[i + 1] == table_graph[j][0] and trail_old[i] == table_graph[j][1]:
                length_route += table_graph[j][2]
    return length_route, trail_old


def random_change_road(mass_all_trail, mass_iteration):
    trail_change_mass = mass_all_trail[-1]
    mass_to_changes = False
    while mass_to_changes is not True:
        first_number = round(random.randrange(1, 6))
        second_number = round(random.randrange(1, 6))
        if first_number != second_number:
            for i in range(len(trail_change_mass)):
                if trail_change_mass[i] == second_number:
                    trail_change_mass[i] = first_number
                elif trail_change_mass[i] == first_number:
                    trail_change_mass[i] = second_number
            if trail_change_mass in mass_all_trail:
                mass_to_changes = True
                mass_all_trail.append(trail_change_mass)
    print(f'Рассмотрим путь №{mass_iteration[-1]} = ', end='')
    for i in trail_change_mass:
        print(i, end=' -> ')
    print()
    return trail_change_mass


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
