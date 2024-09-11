import json
from .paths import ROOT_DIR
class Parser:
    pass

class FileManager:
    def __init__(self):
        pass

    def write(self, filename):
        pass

    def read(self):
        pass


    def write_json_with_pos(self, graph:list[tuple[float, tuple[int, int], tuple[int, int]]], filepath="dataGraph.json"):
        if len(graph) < 1:
            return
        with open(filepath, "w") as f:

            json.dump(graph, f, indent=4)


    def read_json_with_pos(self, filepath="dataGraph.json"):
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        return data

    def write_to_txt(self, graph:list[tuple[float, tuple[int, int], tuple[int, int]]], filepath="dataGraph.txt"):
        with open(filepath, "w") as file:
            for edge in graph:
                file.write(f"{edge[0]} {edge[1][0]} {edge[1][1]} {edge[2][0]} {edge[2][1]}\n")

    def read_txt_with_pos(self, filepath="dataGraph.txt"):
        data = []
        with open(filepath, "r") as file:
            text = file.read().strip().split("\n")
            for i in text:
                row = i.split(" ")
                # print(row)
                data.append(( float(row[0]), (int(row[1]), int(row[2])), (int(row[3]), int(row[4]))  ))

        return data


if __name__ == "__main__":

    f = FileManager()
    # f.write_json_with_pos(filepath=ROOT_DIR/"dataGraph.json", graph=[((123, 321), (0.23, 1, 2)), ((145, 521), (0.73, 2, 3)), ((45, 121), (0.8, 3, 1))])
    # g = json.loads("""
    #
    #                                 [
    #                                 [
    #                                     1.0,
    #                                     [
    #                                         536,
    #                                         226
    #                                     ],
    #                                     [
    #                                         755,
    #                                         350
    #                                     ]
    #                                 ],
    #                                 [
    #                                     0.2,
    #                                     [
    #                                         41,
    #                                         325
    #                                     ],
    #                                     [
    #                                         532,
    #                                         84
    #                                     ]
    #                                 ],
    #                                 [
    #                                     0.3,
    #                                     [
    #                                         163,
    #                                         121
    #                                     ],
    #                                     [
    #                                         324,
    #                                         99
    #                                     ]
    #                                 ],
    #                                 [
    #                                     0.4,
    #                                     [
    #                                         163,
    #                                         121
    #                                     ],
    #                                     [
    #                                         41,
    #                                         325
    #                                     ]
    #                                 ],
    #                                 [
    #                                     3.0,
    #                                     [
    #                                         536,
    #                                         226
    #                                     ],
    #                                     [
    #                                         532,
    #                                         84
    #                                     ]
    #                                 ]
    #                             ]
    #                                 """
    #                         )
    # f.write_to_txt(filepath=ROOT_DIR/"dataGraph.txt", graph=g)
    #
    f.read_txt_with_pos(filepath=ROOT_DIR/"dataGraph.txt")
