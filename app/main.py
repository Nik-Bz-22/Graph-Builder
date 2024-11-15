import _tkinter
import math
import tkinter as tk
from dataclasses import dataclass
from tkinter import simpledialog, Menu
from typing_extensions import Callable

from .Graph.Node.node import Node
from .Graph.Edge.edge import Edge
from .Utils.CustomNotebook import CustomNotebook
from .Utils.SelectionArea import SelectionArea
from .Utils.file_manager import FileManager
from .Algoritms.main import Algorithms, GRAPH_TYPE


@dataclass
class Meta:
    nodes: list[Node]
    edges: list[Edge]
    select: SelectionArea


class MouseHandler:
    def __init__(self):
        self.dragging_node: Node = None
        self.selectedNode = None
        self.edges: list = []
        self.connecting: bool = False
        self.canvas = None
        self.num_of_nodes: int = 0
        self.nodes: list = []
        self.selectedNodes: list = []
        self.undo_stack = []

    def on_mouse_drag(self, event):
        if isinstance(self, GBuilder):
            if not hasattr(self, "initial_drag_coords"):
                self.initial_drag_coords = {
                    "mouse_x": event.x,
                    "mouse_y": event.y,
                    "nodes": [],
                }
                for n in self.meta.select.nodes:
                    if n.is_selected:
                        self.initial_drag_coords["nodes"].append(
                            {"node": n, "x": n.x, "y": n.y}
                        )

            dx = event.x - self.initial_drag_coords["mouse_x"]
            dy = event.y - self.initial_drag_coords["mouse_y"]

            for entry in self.initial_drag_coords["nodes"]:
                node = entry["node"]
                initial_x = entry["x"]
                initial_y = entry["y"]

                new_x = initial_x + dx
                new_y = initial_y + dy

                self.canvas.coords(
                    node.oval,
                    new_x - node.r,
                    new_y - node.r,
                    new_x + node.r,
                    new_y + node.r,
                )

                node.x = new_x
                node.y = new_y

                node.update_edges()
                node.update_node(new_x, new_y)

    def on_mouse_release(self, event):
        if hasattr(self, "initial_drag_coords"):
            del self.initial_drag_coords
        for n in self.meta.select.nodes:
            n.deselect()

    # TODO: add functionality to revert changes by clicking on Crtl + Z

    def add_random_node(self):
        if isinstance(self, GBuilder):
            new_node = Node(x=100, y=100, index=1000, canvas_name=self.canvas)
            # print(new_node)
            self.add_node(new_node)

    def add_node(self, node: Node):
        if isinstance(self, GBuilder):
            self.nodes.append(node)
            self.meta.select.nodes.append(node)
        else:
            self.nodes.append(node)

    def add_nodes(self, nodes: list[Node]):
        for n in nodes:
            self.add_node(n)

    def double_right_click(self, event):
        if self.connecting:
            return
        for n in self.nodes:
            if n.is_collide(event.x, event.y):
                return
        self.num_of_nodes += 1
        new_node = Node(event.x, event.y, self.num_of_nodes, self.canvas)
        self.add_node(new_node)

    def canvas_mouse_right_click(self, event):
        for n in self.nodes:
            if n.is_clicked(event.x, event.y):
                if self.connecting:
                    self.selectedNode.clicked_up()

                    if n is not self.selectedNode:
                        new_edge = Edge(self.selectedNode, n, self.canvas)
                        self.edges.append(new_edge)
                    self.connecting = False

                else:
                    n.select()
                    self.selectedNode = n
                    self.connecting = True
                    # self.selectedNodes.append(n)

    def on_left_click(self, event):
        self.connecting = False

        for n in self.nodes:
            if n.is_clicked(event.x, event.y):
                n.select()
                self.selectedNodes.append(n)
                return

    # def del_node(self, event):
    #     to_del = []
    #     for n in self.nodes:
    #         if n.is_selected:
    #             for edge in n.edges:
    #                 try:
    #                     self.edges.remove(edge)
    #                     edge.delete()

    #                 except ValueError:
    #                     pass
    #             n.delete()
    #             to_del.append(n)

    #     for nn in to_del:
    #         self.nodes.remove(nn)

    def del_node(self, event):
        to_del = []
        deleted_data = []  # To store information about deleted nodes and edges
        for n in self.nodes:
            if n.is_selected:
                deleted_edges = []
                for edge in n.edges:
                    try:
                        self.edges.remove(edge)
                        edge.delete()
                        deleted_edges.append(edge)
                    except ValueError:
                        pass
                n.delete()
                to_del.append(n)
                deleted_data.append((n, deleted_edges))

        for nn in to_del:
            self.nodes.remove(nn)

        # Add the deleted data to the undo stack
        if deleted_data:
            self.undo_stack.append(deleted_data)

    def select_all(self, event):
        for n in self.nodes:
            n.select()

    def rotate_selected_part(self, event):
        self.selected_node = self.selectedNode
        center_x, center_y = self.selected_node.x, self.selected_node.y
        angle_degrees = 5
        angle_radians = math.radians(angle_degrees)

        for node in self.nodes:
            if node != self.selected_node:
                x, y = node.x, node.y

                x_shifted = x - center_x
                y_shifted = y - center_y

                new_x = round(
                    x_shifted * math.cos(angle_radians)
                    - y_shifted * math.sin(angle_radians)
                )
                new_y = round(
                    x_shifted * math.sin(angle_radians)
                    + y_shifted * math.cos(angle_radians)
                )

                node.x, node.y = (new_x + center_x, new_y + center_y)

                node.update_node(new_x + center_x, new_y + center_y)
                node.update_edges()


class GBuilder(MouseHandler):
    class CallBacker:
        def __init__(self, builder):
            def temp(e):
                builder.connecting = False
                builder.meta.select.on_mouse_down_s(e)

            builder.canvas.bind("<Button-1>", lambda e: temp(e))
            builder.canvas.bind("<B1-Motion>", builder.meta.select.on_mouse_drag)
            builder.canvas.bind(
                "<ButtonRelease-1>", builder.meta.select.on_mouse_release
            )
            builder.canvas.bind("<Control-a>", builder.select_all)
            builder.canvas.bind("<Control-r>", builder.rotate_selected_part)

            builder.canvas.bind("<Double-Button-3>", builder.double_right_click)
            # add event handlers for key "a"
            builder.canvas.bind("<a>", builder.double_right_click)
            # builder.canvas.bind("<Control-z>", builder.undo)

            builder.canvas.tag_bind(
                "node", "<Button-3>", builder.canvas_mouse_right_click
            )
            builder.canvas.tag_bind("node", "<B1-Motion>", builder.on_mouse_drag)
            builder.canvas.tag_bind(
                "node", "<ButtonRelease-1>", builder.on_mouse_release
            )
            builder.canvas.tag_bind("node", "<Button-1>", builder.on_left_click)
            # builder.canvas.tag_bind("node", "<Double-1>", builder.double_left_click)
            builder.canvas.bind("<Delete>", builder.del_node)

    def __init__(self, tab, root):
        super().__init__()
        self.root = root
        self.tab = tab
        self.canvas = tk.Canvas(self.tab, bg="white")

        self.file_manager = FileManager()
        self.meta = Meta(self.nodes, self.edges, SelectionArea(self.canvas))
        self.active_tab = 0

        self.screen_width = self.tab.winfo_screenwidth()
        self.screen_height = self.tab.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.CallBacker(self)

        self.from_file = None

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
        self.connecting = False
        self.selectedNode = None

    # TODO:
    # def undo(self, event):
    #     if not self.undo_stack:
    #         print("Undo")
    #         return
    #
    #     deleted_data = self.undo_stack.pop()
    #     # print(deleted_data)
    #     for node, edges in deleted_data:
    #         # print(node, edges)
    #         print(node.x)
    #         print(node.y)
    #         print(node.index)
    #         print(node.canvas_name)
    #         self.add_node(node)
    #         # Restore the node
    #         # self.nodes.append(node)
    #         # node.redraw()
    #
    #         # for edge in edges:
    #         #     self.edges.append(edge)
    #         #     edge.redraw()
    #
    #     self.canvas.update()

    def get_graph(self) -> GRAPH_TYPE:
        graph: GRAPH_TYPE = []
        for e in self.edges:
            graph.append((e.weight, (e.node1.x, e.node1.y), (e.node2.x, e.node2.y)))
        return graph

    def print_graph_on(self, on, graph: GRAPH_TYPE):
        # self.canvas.delete("all")
        nodes: set[Node] = set()
        local_edges = dict()
        for edge in graph:
            node1_coords = edge[1]
            node2_coords = edge[2]

            n1 = next(
                (n for n in nodes if n.x == node1_coords[0] and n.y == node1_coords[1]),
                None,
            )
            if n1 is None:
                n1 = Node(
                    x=node1_coords[0],
                    y=node1_coords[1],
                    index=self.integer_generator(),
                    canvas_name=on,
                )
                nodes.add(n1)

            n2 = next(
                (n for n in nodes if n.x == node2_coords[0] and n.y == node2_coords[1]),
                None,
            )
            if n2 is None:
                n2 = Node(
                    x=node2_coords[0],
                    y=node2_coords[1],
                    index=self.integer_generator(),
                    canvas_name=on,
                )
                nodes.add(n2)

            local_edges[(n1, n2)] = edge[0]

        for n1, n2 in local_edges:
            self.edges.append(Edge(n1, n2, self.canvas, local_edges[(n1, n2)]))

        self.add_nodes(list(nodes))


class App:
    def __init__(self, root):
        self.console = None
        self.context_menu = None
        self._root = root
        self.bg_image = None
        self.bg_images = []  # Ensure this line is there
        self.notebook = CustomNotebook(self._root)
        self.main_tab = tk.Canvas(self.notebook)
        self.notebook.add(self.main_tab, text="MainWindow")
        self.current_tab_index = self.notebook.index(self.main_tab)
        self.builders = {}

        self.builders.update(
            {self.current_tab_index: GBuilder(self.main_tab, self._root)}
        )
        self.notebook.pack(expand=True, fill="both")

        self.mainmenu = Menu(self._root)
        self.algorithms = Algorithms()

        self.builder = self.builders[self.current_tab_index]

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.notebook.bind("<Button-3>", self.show_context_menu)

        self.menus = []

    def init_menu(self):
        filemenu = Menu(self.mainmenu, tearoff=0)
        filemenu.add_command(label="Open", command=lambda: self.open_graph())
        filemenu.add_command(label="Save", command=lambda: self.save_graph())
        filemenu.add_command(label="Save as", command=lambda: self.save_as())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=exit)

        self.menus.append(filemenu)

        algomenu = Menu(self.mainmenu, tearoff=0)
        algomenu.add_command(
            label="Min tree",
            command=lambda: self.execute_algorithm(self.algorithms.min_tree),
        )
        algomenu.add_command(
            label="Max tree",
            command=lambda: self.execute_algorithm(self.algorithms.max_tree),
        )
        algomenu.add_command(
            label="Randic index",
            command=lambda: self.execute_algorithm(self.algorithms.radic_index),
        )
        algomenu.add_command(
            label="Calculate weight",
            command=lambda: self.execute_algorithm(
                self.algorithms.calc_weight, new_tab=False
            ),
        )
        algomenu.add_command(
            label="Get invariant",
            command=lambda: self.execute_algorithm(
                self.algorithms.get_invariant, new_tab=False
            ),
        )

        self.menus.append(algomenu)

        toolmenu = Menu(self.mainmenu, tearoff=0)
        toolmenu.add_command(label="Add new tab", command=self.add_new_tab)
        toolmenu.add_command(label="Add new Node", command=self.add_r_node)
        toolmenu.add_command(label="Load background image", command=self.load_bg_image)

        self.menus.append(toolmenu)

        self.mainmenu.add_cascade(label="File", menu=filemenu)
        self.mainmenu.add_cascade(label="Algorithms", menu=algomenu)
        self.mainmenu.add_cascade(label="Tools", menu=toolmenu)

        self.context_menu = tk.Menu(self._root, tearoff=0)
        self.context_menu.add_command(
            label="Close tab", command=lambda: self.close_tab()
        )
        self.context_menu.add_command(label="Rename", command=lambda: self.rename_tab())

        self.menus.append(self.context_menu)

    def close_tab(self):
        notebook = self.notebook
        current_tab = notebook.index(notebook.select())
        notebook.forget(current_tab)

    def rename_tab(self):
        notebook = self.notebook
        current_tab = notebook.index(notebook.select())
        new_name = simpledialog.askstring("Input", "Enter the new name")
        notebook.tab(current_tab, text=new_name)

    def show_context_menu(self, event):
        notebook = self.notebook

        try:
            try:
                tab_id = notebook.index(f"@{event.x},{event.y}")
            except _tkinter.TclError:
                self.context_menu.tk_popup(event.x_root, event.y_root)
                return

            notebook.select(tab_id)
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def add_new_tab(self):
        new_tab = tk.Canvas(self.notebook, bg="lightgray")
        b = GBuilder(new_tab, self._root)
        self.notebook.add(new_tab, text=f"Tab #{str(len(self.notebook.tabs()))}")
        self.builders.update({self.notebook.index(new_tab): b})
        return b

    def add_r_node(self):
        self.builder.add_random_node()

    def load_bg_image(self):
        bg_image_path = self.builder.file_manager.get_path_to_image()
        bg = tk.PhotoImage(file=bg_image_path)
        self.builder.canvas.bg_id = self.builder.canvas.create_image(
            0, 0, image=bg, anchor="nw"
        )
        self.builder.canvas.bg_image = bg

    def save_graph(self):
        graph = self.builder.get_graph()
        if not self.builder.from_file:
            self.builder.file_manager.save_as(graph)
            return
        self.builder.file_manager.write_to_txt(graph, self.builder.from_file)

    def execute_algorithm(self, algorithm: Callable, new_tab=True) -> None:
        input_graph_data = self.builder.get_graph()
        result = algorithm(input_graph_data)

        if new_tab:
            builder = self.add_new_tab()

            builder.print_graph_on(builder.canvas, result["graph"])
            if result["data"]:
                self.console.write_line(result["data"])
            return

        self.console.write_line(result["data"])

    def open_graph(self):
        data_from_open = self.builder.file_manager.open_file()
        graph: GRAPH_TYPE = data_from_open["graph"]
        filepath = data_from_open["filepath"]
        self.builder.print_graph_on(self.builder.canvas, graph)
        self.builder.from_file = filepath

    def save_as(self):
        graph: GRAPH_TYPE = self.builder.get_graph()
        filepath = self.builder.file_manager.save_as(graph)
        self.builder.from_file = filepath

    def on_tab_change(self, event):
        self.current_tab_index = self.notebook.index("current")
        self.builder = self.builders[self.current_tab_index]
        self.builder.canvas.focus_set()

    class Console:
        def __init__(self, root):
            self.root = root
            self.console = tk.Text(self.root, height=4, font=("Arial", 16))
            self.console.pack(fill=tk.X)
            self.clear_button = tk.Button(
                root,
                text="X",
                command=self.clear_text,
                fg="white",
                relief=tk.FLAT,
                width=1,
                height=1,
                padx=10,
                pady=3,
                font=("Arial", 16),
                borderwidth=0,
            )
            self.update_button_position()

        @staticmethod
        def _console_modify(method):
            def wrapper(self, *args, **kwargs):
                self.console.config(state=tk.NORMAL)
                method(self, *args, **kwargs)
                self.console.config(state=tk.DISABLED)

            return wrapper

        @_console_modify
        def write_line(self, text):
            self.console.insert(tk.END, f">>>  {str(text)}\n")

        @_console_modify
        def clear_text(self):
            self.console.delete(1.0, tk.END)

        def update_button_position(self, event=None):
            self.console.update_idletasks()
            x = self.console.winfo_x()
            y = self.console.winfo_y()
            width = self.console.winfo_width()
            self.clear_button.place(x=x + width - 37, y=y + 2)

    def render(self):
        self._root.config(menu=self.mainmenu)
        self.init_menu()
        btn_frame = tk.Frame(self._root, bg="#f2eb22")
        btn_frame.pack()
        self.console = self.Console(self._root)
        self._root.mainloop()


def main():
    _root = tk.Tk()
    _root.title("Graph Builder")
    _root.resizable(True, True)

    app = App(_root)
    # app.load_bg()
    app.render()
