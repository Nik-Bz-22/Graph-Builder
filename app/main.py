import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from tkinter import simpledialog, Menu
import random

from .Graph.Node.node import Node
from .Graph.Edge.edge import Edge
from .Utils.paths import RESOURCE_FILE
from .Utils.file_manager import FileManager
from .Algoritms.main import Algorithms

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

class SelectionArea:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect_id = None
        self.start_x = None
        self.start_y = None
        self.nodes = []

    def on_mouse_down_s(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black")


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
        # print(self.nodes)
        # Проходим по всем узлам и проверяем, кто попал в выделенную область
        for node in self.nodes:
            if node.is_inside(x1, y1, x2, y2):
                node.select()  # Выделяем узел
                # print(node, "selected")
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
                # print(node, "selected")
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
        self.edges:list = []
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
        # print(clicked_items.x)

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


    def select_all(self, event):
        for n in self.nodes:
            n.select()
            print("select", n)

class GBuilder(MouseHandler):
    def __init__(self, tab, root):
        super().__init__()
        self.root = root
        self.tab = tab
        self.canvas = tk.Canvas(self.tab, bg="#e8b731")
        self.file_manager = FileManager()
        self.meta = Meta(self.nodes, self.edges, SelectionArea(self.canvas))


        self.active_tab = 0



        self.screen_width = self.tab.winfo_screenwidth()
        self.screen_height = self.tab.winfo_screenheight()
        # # print(f"{self.screen_width=}    {self.screen_height=}")
        #
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        # self.nodes = []
        # self.edges = []


        self.canvas.pack(fill=tk.BOTH, expand=True)


        self.canvas.bind("<Button-1>", self.meta.select.on_mouse_down_s)
        self.canvas.bind("<B1-Motion>", self.meta.select.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.meta.select.on_mouse_release)
        # self.canvas.focus_set()
        self.canvas.bind("<Control-a>", self.select_all)
        # root.bind_all("<Control-a>", select_all)

        self.canvas.bind("<Double-Button-3>", self.double_right_click)
        self.canvas.tag_bind("node", "<Button-3>", self.canvas_mouseRightClick)
        self.canvas.tag_bind("node", "<B1-Motion>", self.on_mouse_drag)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.tag_bind("node", "<Button-1>", self.on_double_click)
        self.canvas.tag_bind("node", "<Double-1>", self.double_left_click)
        self.canvas.bind("<Delete>", self.del_node)





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
        print(self, self.nodes)
        self.nodes.clear()
        self.edges.clear()

        self.num_of_nodes = 0

        # 'Connecting Nodes Variables:
        self.connecting = False
        self.selectedNode = None
        # print(self, "clear")

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





class App:
    def __init__(self, root):
        self._root = root
        # self.notebook = ttk.Notebook(self._root)
        self.notebook = CustomNotebook(self._root)
        self.main_tab = tk.Canvas(self.notebook)
        # self.notebook.add(self.main_tab)
        # print(self.notebook.index(self.main_tab))
        self.notebook.add(self.main_tab, text="Main")
        self.current_tab_index = self.notebook.index(self.main_tab)
        self.builders = {}

        self.builders.update({self.current_tab_index: GBuilder(self.main_tab, self._root)})
        self.notebook.pack(expand=True, fill="both")


        self.algorithms = Algorithms()
        self.mainmenu = Menu(self._root)

        self.builder = self.builders[self.current_tab_index]

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # self._root.bind_all("<Control-a>", self.select_all)


    def init_menu(self):
        builder = self.builders[self.current_tab_index]
        # builder = self.builder
        # print(builder)
        filemenu = Menu(self.mainmenu, tearoff=0)
        filemenu.add_command(label="Open Graph", command=lambda: self.load_graph())
        filemenu.add_command(label="Save", command=lambda: self.save_graph())
        filemenu.add_command(label="Save as")
        filemenu.add_separator()
        filemenu.add_command(label="Exit")

        algomenu = Menu(self.mainmenu, tearoff=0)
        algomenu.add_command(label="Kraskal",
                             command=lambda: self.kruskal())

        self.mainmenu.add_cascade(label="File", menu=filemenu)
        self.mainmenu.add_cascade(label="Algorithms", menu=algomenu)


    def add_new_tab(self):
        new_tab = tk.Canvas(self.notebook, bg="lightgray")
        b = GBuilder(new_tab, self._root)
        self.notebook.add(new_tab, text=f"Tab #{str(len(self.notebook.tabs()))}")
        self.builders.update({self.notebook.index(new_tab): b})
        return b

        # import_btn = tk.Button(btn_frame, image=p3, command=lambda: self.notebook.add(new_tab, text="Вкладка 2"))
        # print(self.notebook.index(new_tab))

    def clear_window(self):
        self.builder.clear()

    def load_graph(self):
        self.builder.open_graph()

    def save_graph(self):
        self.builder.save_file()

    def kruskal(self):
        builder = self.add_new_tab()
        builder.print_graph_on(builder.canvas, self.algorithms.kruskal(self.builder.get_graph()))





    def on_tab_change(self, event):
        self.current_tab_index = self.notebook.index("current")
        # print(self.current_tab_index)
        self.builder = self.builders[self.current_tab_index]
        self.builder.canvas.focus_set()
        # print(self.builder)








    def render(self):

        self._root.config(menu=self.mainmenu)

        self.init_menu()





        # print(self.notebook.index(self.main_tab))

        btn_frame = tk.Frame(self._root, bg="#f2eb22")
        btn_frame.pack()

        # p1 = tk.PhotoImage(file=RESOURCE_FILE / "button_export.png")
        # export_btn = tk.Button(btn_frame, image=p1, command=builder.save_file)
        # export_btn.pack(padx=5, pady=10, side=tk.LEFT)

        p2 = tk.PhotoImage(file=RESOURCE_FILE / "button_clear.png")
        clear_btn = tk.Button(btn_frame, image=p2, command=self.clear_window)
        clear_btn.pack(padx=5, pady=10, side=tk.LEFT)

        # Add the import buttun for import graph to workspace
        p3 = tk.PhotoImage(file=RESOURCE_FILE / "button_clear.png")

        # import_btn = tk.Button(btn_frame, image=p3, command=lambda: builder.print_graph_on(builder.canvas))
        # new_tab = tk.Canvas(self.notebook, bg="lightgray")
        # b = GBuilder(new_tab, self._root)

        import_btn = tk.Button(btn_frame, image=p3, command=lambda: self.add_new_tab())
        # self.builders.update({self.notebook.index(new_tab): b})
        # print(self.notebook.index(new_tab))


        # Добавляем элемент на Canvas
        # tab2.create_text(100, 50, text="Содержимое второй вкладки", fill="black"))
        import_btn.pack(padx=5, pady=10, side=tk.LEFT)

        self._root.mainloop()


def main():
    _root = tk.Tk()
    _root.title("Graph Builder")
    _root.resizable(True, True)
    _root.configure(background="#f2eb22")



    app = App(_root)
    app.render()








