import tkinter as tk
from dataclasses import dataclass
from tkinter import simpledialog, Menu
import random

from .Graph.Node.node import Node
from .Graph.Edge.edge import Edge
from .Utils.paths import RESOURCE_FILE
from .Utils.file_manager import FileManager
from .Algoritms.main import Algorithms



class SelectionArea:
    def __init__(self, canvas):
        """
        Класс для выделения объектов в прямоугольной области на указанном холсте (Canvas).
        """
        self.canvas = canvas
        self.rect_id = None  # ID для прямоугольника выделения
        self.start_x = None
        self.start_y = None
        self.nodes = []

        # Привязываем события мыши
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_down(self, event):

        """Начало выделения."""
        self.start_x = event.x
        self.start_y = event.y
        # Создаем прямоугольник выделения
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black")
        # for n in self.nodes:
        #     if n.is_clicked(event.x, event.y):
        #         self.dragging_node = None
        #         return


    def on_mouse_drag(self, event):
        """Обновление прямоугольника выделения при перетаскивании."""
        cur_x, cur_y = event.x, event.y
        # Обновляем прямоугольник выделения
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_release(self, event):
        """Завершение выделения и проверка, какие узлы попали в область."""
        end_x, end_y = event.x, event.y

        # Получаем координаты выделенной области
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        print(self.nodes)
        # Проходим по всем узлам и проверяем, кто попал в выделенную область
        for node in self.nodes:
            if node.is_inside(x1, y1, x2, y2):
                node.select()  # Выделяем узел
                print(node, "selected")
            else:
                node.deselect()  # Снимаем выделение с узла

        # Удаляем прямоугольник выделения
        self.canvas.delete(self.rect_id)
        self.rect_id = None

    def on_mouse_release2(self, event):

        end_x, end_y = event.x, event.y

        # Получаем координаты выделенной области
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)

        for node in self.nodes:
            if node.is_inside(x1, y1, x2, y2):
                node.select()  # Выделяем узел
                print(node, "selected")
            else:
                node.deselect()






@dataclass
class Meta:
    nodes:list[Node]
    edges:list[Edge]
    select: SelectionArea




class MouseHandler:
    def __init__(self):
        self.dragging_node = None
        self.selectedNode = None
        self.edges:list = None
        self.connecting:bool = None
        self.canvas = None
        self.num_of_nodes = None
        self.nodes:list = []
        # self.selecter = SelectionArea()


    def add_node(self, node: Node):
        if isinstance(self, GBuilder):
            self.nodes.append(node)
            # print(self.meta)
            self.meta.select.nodes.append(node)
        else:
            self.nodes.append(node)
            # self.meta.nodes.append(node)


    def add_nodes(self, nodes:list[Node]):
        for n in nodes:
            self.add_node(n)

    def double_right_click(self, event):
        if self.connecting:
            return
        # 'Check for collision:
        for n in self.nodes:
            if n.is_collide(event.x, event.y):
                return
        # 'Add new node:
        self.num_of_nodes += 1
        new_node = Node(event.x, event.y, self.num_of_nodes, self.canvas)
        self.add_node(new_node)


    def double_left_click(self, event):
        clicked_items = self.canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
        print(clicked_items.x)

    def canvas_mouseRightClick(self, event):
        for n in self.nodes:
            if n.is_clicked(event.x, event.y):
                if self.connecting:
                    self.selectedNode.clicked_up()
                    if n is not self.selectedNode:
                        # Создание ребра с дефолтным весом 0
                        new_edge = Edge(self.selectedNode, n, self.canvas)
                        self.edges.append(new_edge)
                    self.connecting = False
                else:
                    n.select()
                    self.selectedNode = n
                    self.connecting = True

    def on_double_click(self, event):
        for n in self.nodes:
            if n.is_clicked(event.x, event.y):
                self.dragging_node = n
                return

    def on_mouse_drag(self, event):
        if self.dragging_node:
            self.canvas.coords(self.dragging_node.oval,
                               event.x - self.dragging_node.r,
                               event.y - self.dragging_node.r,
                               event.x + self.dragging_node.r,
                               event.y + self.dragging_node.r)
            self.dragging_node.x = event.x
            self.dragging_node.y = event.y
            self.dragging_node.update_edges()  # Обновляем все ребра, связанные с узлом
            self.dragging_node.update_node(event.x, event.y)  # Обновляем текст узла

    def on_mouse_release(self, event):
        self.dragging_node = None


    def del_node(self, event):
        to_del = []
        for n in self.nodes:
            if n.is_selected:
                for edge in n.edges:
                    try:
                        self.edges.remove(edge)
                        edge.delete()

                    except ValueError:
                        pass
                n.delete()
                to_del.append(n)
                # self.nodes.remove(n)
                # del n
        for nn in to_del:
            self.nodes.remove(nn)




        # if self.connecting:
        #     print(self.edges)
        #     # Удаляем все инцидентные ребра
        #     for edge in self.selectedNode.edges:
        #         try:
        #             self.edges.remove(edge)
        #             edge.delete()
        #
        #         except ValueError:
        #             pass
        #     # self.selectedNode.edges.clear()
        #
        #
        #     # Удаляем сам узел
        #     self.selectedNode.delete()
        #     self.nodes.remove(self.selectedNode)
        #     self.selectedNode = None
        #     self.connecting = False
        #     # self.num_of_nodes -= 1
        #






class GBuilder(MouseHandler):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.canvas = tk.Canvas(root, bg="#f7f7f5")
        self.file_manager = FileManager()
        self.meta = Meta(self.nodes, self.edges, SelectionArea(self.canvas))



        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        # print(f"{self.screen_width=}    {self.screen_height=}")

        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.nodes = []
        self.edges = []


        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Double-Button-3>", self.double_right_click)
        self.canvas.tag_bind("node", "<Button-3>", self.canvas_mouseRightClick)
        self.canvas.tag_bind("node", "<B1-Motion>", self.on_mouse_drag)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.tag_bind("node", "<Button-1>", self.on_double_click)
        self.root.bind("<Delete>", self.del_node)
        self.canvas.tag_bind("node", "<Double-1>", self.double_left_click)





        self.num_of_nodes = 0

        self.dragging_node = None

        # 'Connecting Nodes Variables:
        self.connecting = False
        self.selectedNode:Node = None

    def integer_generator(self, start=0, step=1):
        current = start
        while True:
            yield current
            current += step


    def clear(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()

        self.num_of_nodes = 0

        # 'Connecting Nodes Variables:
        self.connecting = False
        self.selectedNode = None

    def export(self):
        if self.num_of_nodes < 1:
            return
        with open("../model.txt", "w+") as f:
            f.write("#{0}\n".format(self.num_of_nodes))
            for e in self.edges:
                f.write("{0} {1} {2}\n".format(e.node1.index, e.node2.index, e.weight))
            f.write("---")


    def get_graph(self):
        graph = []
        # for i in self.edges:
        #     graph.update(list( tuple(i.node1.x, i.node1.y), tuple(i.node1.index, i.node2.index, i.weight)))
        # graph_data = []
        #
        # # Создаем словарь для быстрого поиска узлов по их индексам
        # node_dict = {node.index: (node.x, node.y) for node in self.nodes}
        # print(node_dict)
        #
        # for edge in self.edges:
        #     node1_index = edge.node1.index
        #     node2_index = edge.node2.index
        #     weight = edge.weight
        #     x1, y1 = node_dict[node1_index]
        #     x2, y2 = node_dict[node2_index]
        #
        #     edge_data = [[x1, y1], [weight, node1_index, node2_index]]
        #     graph_data.append(edge_data)
        #
        #     edge_data = [[x2, y2], [weight, node2_index, node1_index]]
        #     graph_data.append(edge_data)
        for e in self.edges:
            graph.append((e.weight, (e.node1.x, e.node1.y), (e.node2.x, e.node2.y)))



        return graph

    # def print_graph_on(self, on, graph:list[ list[list[int, int], list[float, int, int]] ]):
    #     nodes = {}
    #
    #     work_field_width = on.winfo_width()
    #     work_field_height = on.winfo_height()
    #
    #
    #     new_color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    #     # Создаем узлы и сохраняем их в словарь
    #     # for weight, node1_index, node2_index in graph:
    #     #     if node1_index not in nodes:
    #     #         nodes[node1_index] = Node(x=random.randint(10, work_field_width-12), y=random.randint(10, work_field_height-10), index=node1_index, canvas_name=on, color=new_color)
    #     #         self.num_of_nodes += 1
    #     #     if node2_index not in nodes:
    #     #         nodes[node2_index] = Node(x=random.randint(10, work_field_width-12), y=random.randint(10, work_field_height-10), index=node2_index, canvas_name=on, color=new_color)
    #     #         self.num_of_nodes += 1
    #
    #     for coord, node in graph:
    #
    #         if node[1] not in nodes:
    #             nodes[node[1]] = Node(x=coord[0], y=coord[1], index=node[1], canvas_name=on, color=new_color)
    #             self.num_of_nodes += 1
    #         if node[2] not in nodes:
    #             nodes[node[2]] = Node(x=coord[0], y=coord[1], index=node[2], canvas_name=on, color=new_color)
    #             self.num_of_nodes += 1
    #
    #     local_edges = []
    #     # winfo_height size winfo_width winfo_x winfo_y
    #     # Создаем и рисуем ребра
    #     # for weight, node1_index, node2_index in graph:
    #     #
    #     #     node1 = nodes[node1_index]
    #     #     node2 = nodes[node2_index]
    #     #
    #     #     # Создаем ребро с весом
    #     #     edge = Edge(node1, node2, on, weight=weight)
    #     #     local_edges.append(edge)
    #
    #
    #     for coord, node in graph:
    #
    #         node1 = nodes[node[1]]
    #         node2 = nodes[node[2]]
    #
    #         # Создаем ребро с весом
    #         edge = Edge(node1, node2, on, weight=node[0])
    #         local_edges.append(edge)
    #
    #     self.edges.extend(local_edges)
    #     self.nodes.extend(nodes.values())

    def save_file(self):
        gr = self.get_graph()
        print("Graph to save:  ", gr)
        self.file_manager.write_to_txt(gr)

    def open_graph(self):
        graph = self.file_manager.read_txt_with_pos()
        print("Graph to open:  ", graph)

        self.print_graph_on(self.canvas, graph)


    def print_graph_on(self, on, graph:list[tuple[float, tuple[int, int], tuple[int, int]]]=[(0.2, (123, 321), (200, 100)), (0.3, (163, 121), (150, 210)), (0.4, (163, 121), (123, 321))]):
        self.canvas.delete("all")
        nodes = set()
        local_edges = dict()

        for edge in graph:
            node1_coords = edge[1]
            node2_coords = edge[2]

            # Найдем или создадим узел n1
            n1 = next((n for n in nodes if n.x == node1_coords[0] and n.y == node1_coords[1]), None)
            if n1 is None:
                n1 = Node(x=node1_coords[0], y=node1_coords[1], index=self.integer_generator(), canvas_name=on)
                nodes.add(n1)

            # Найдем или создадим узел n2
            n2 = next((n for n in nodes if n.x == node2_coords[0] and n.y == node2_coords[1]), None)
            if n2 is None:
                n2 = Node(x=node2_coords[0], y=node2_coords[1], index=self.integer_generator(), canvas_name=on)
                nodes.add(n2)

            local_edges[(n1, n2)] = edge[0]

        for n1, n2 in local_edges:
            self.edges.append(Edge(n1, n2, self.canvas, local_edges[(n1, n2)]))

        self.add_nodes(list(nodes))
        # self.nodes.extend(list(nodes))





def main():
    a = Algorithms()
    _root = tk.Tk()
    _root.title("Graph Builder")
    _root.resizable(True, True)
    _root.configure(background="#f2eb22")
    mainmenu = Menu(_root)
    _root.config(menu=mainmenu)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Open Graph", command=lambda: builder.open_graph())
    filemenu.add_command(label="Save", command=lambda: builder.save_file())
    filemenu.add_command(label="Save as")
    filemenu.add_separator()
    filemenu.add_command(label="Exit")

    algomenu = Menu(mainmenu, tearoff=0)



    algomenu.add_command(label="Kraskal", command=lambda: builder.print_graph_on(builder.canvas, a.kruskal(builder.get_graph())))

    mainmenu.add_cascade(label="File", menu=filemenu)
    mainmenu.add_cascade(label="Algorithms", menu=algomenu)
    # menubar.add_command(label="File", command=lambda : print("hi"))
    # menubar.add_command(label="Algoritms", command=lambda : print("By"))






    # _root
    builder = GBuilder(_root)



    # menu_frame = tk.Canvas(_root, width=200, height=200)
    # menu_frame.pack(side=tk.RIGHT, padx=5, pady=100)

    btn_frame = tk.Frame(_root, bg="#f2eb22")
    btn_frame.pack()

    p1 = tk.PhotoImage(file=RESOURCE_FILE / "button_export.png")
    export_btn = tk.Button(btn_frame, image=p1, command=builder.save_file)
    export_btn.pack(padx=5, pady=10, side=tk.LEFT)

    p2 = tk.PhotoImage(file=RESOURCE_FILE / "button_clear.png")
    clear_btn = tk.Button(btn_frame, image=p2, command=builder.clear)
    clear_btn.pack(padx=5, pady=10, side=tk.LEFT)

    # Add the import buttun for import graph to workspace
    p3 = tk.PhotoImage(file=RESOURCE_FILE / "button_clear.png")



    import_btn = tk.Button(btn_frame, image=p3, command=lambda: builder.print_graph_on(builder.canvas))
    import_btn.pack(padx=5, pady=10, side=tk.LEFT)




    _root.mainloop()



