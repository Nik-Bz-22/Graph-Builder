import json
import networkx as nx
from app.Algoritms.base import BasedAlgorithm


class Kruskal(BasedAlgorithm):
    def kruskal1(self, graph):

        # graph = json.loads(graph)

        sorted_graph = sorted(graph, key=lambda x: x[0])
        # sorted_graph = sorted(graph, key=lambda x: x[1][0])

        U = set()
        D = {}
        T = []

        # for r in sorted_graph:
        #     if r[1] not in U or r[2] not in U:
        #         if r[1] not in U and r[2] not in U:
        #             D[r[1]] = [r[1], r[2]]
        #             D[r[2]] = D[r[1]]
        #         else:  # иначе
        #             if not D.get(r[1]):
        #                 D[r[2]].append(r[1])
        #                 D[r[1]] = D[r[2]]
        #             else:
        #                 D[r[1]].append(r[2])
        #                 D[r[2]] = D[r[1]]
        #
        #         T.append(r)
        #         U.add(r[1])
        #         U.add(r[2])
        #
        # for r in sorted_graph:
        #     if r[2] not in D[r[1]]:
        #         T.append(r)
        #         gr1 = D[r[1]]
        #         D[r[1]] += D[r[2]]
        #         D[r[2]] += gr1




        # for r in sorted_graph:
        #     if r[1][1] not in U or r[1][2] not in U:
        #         if r[1][1] not in U and r[1][2] not in U:
        #             D[r[1][1]] = [r[1][1], r[1][2]]
        #             D[r[1][2]] = D[r[1][1]]
        #         else:  # иначе
        #             if not D.get(r[1][1]):
        #                 D[r[1][2]].append(r[1][1])
        #                 D[r[1][1]] = D[r[1][2]]
        #             else:
        #                 D[r[1][1]].append(r[1][2])
        #                 D[r[1][2]] = D[r[1][1]]
        #
        #         T.append(r)
        #         U.add(r[1][1])
        #         U.add(r[1][2])
        #
        # for r in sorted_graph:
        #     if r[1][2] not in D[r[1][1]]:
        #         T.append(r)
        #         gr1 = D[r[1][1]]
        #         D[r[1][1]] += D[r[1][2]]
        #         D[r[1][2]] += gr1

        for r in graph:
            if r[1] not in U or r[2] not in U:  # проверка для исключения циклов в остове
                if r[1] not in U and r[2] not in U: # если обе вершины не соединены, то
                    D[r[1]] = [r[1], r[2]]          # формируем в словаре ключ с номерами вершин
                    D[r[2]] = D[r[1]]               # и связываем их с одним и тем же списком вершин
                else:                           # иначе
                    if not D.get(r[1]):             # если в словаре нет первой вершины, то
                        D[r[2]].append(r[1])        # добавляем в список первую вершину
                        D[r[1]] = D[r[2]]           # и добавляем ключ с номером первой вершины
                    else:
                        D[r[1]].append(r[2])        # иначе, все то же самое делаем со второй вершиной
                        D[r[2]] = D[r[1]]

                T.append(r)             # добавляем ребро в остов
                U.add(r[1])             # добавляем вершины в множество U
                U.add(r[2])

        for r in graph:    # проходим по ребрам второй раз и объединяем разрозненные группы вершин
            if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
                T.append(r)             # добавляем ребро в остов
                gr1 = D[r[1]]
                D[r[1]] += D[r[2]]      # объединем списки двух групп вершин
                D[r[2]] += gr1


        print(graph)
        print(T)

        return T

    def kruskal(self, graph):
        G = nx.Graph()

        # Добавляем рёбра
        for weight, node1, node2 in graph:
            G.add_edge(node1, node2, weight=weight)

        # Алгоритм Краскала для минимального остовного дерева
        mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

        # Преобразование результата в исходный формат
        mst_edges = [(data['weight'], node1, node2) for node1, node2, data in mst.edges(data=True)]
        return  mst_edges


if __name__ == "__main__":
    import networkx as nx

    # Данные графа
    edges = [
        (1.0, (475, 189), (755, 350)),
        (0.2, (41, 325), (375, 617)),
        (0.3, (163, 121), (324, 99)),
        (0.4, (163, 121), (41, 325)),
        (3.0, (475, 189), (375, 617)),
        (0.1, (163, 121), (475, 189))
    ]

    # Создаем граф
    G = nx.Graph()

    # Добавляем рёбра
    for weight, node1, node2 in edges:
        G.add_edge(node1, node2, weight=weight)

    # Алгоритм Краскала для минимального остовного дерева
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    # Преобразование результата в исходный формат
    mst_edges = [(data['weight'], node1, node2) for node1, node2, data in mst.edges(data=True)]

    # Вывод в исходном формате
    print(mst_edges)


