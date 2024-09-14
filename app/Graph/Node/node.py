class Node:
    def __init__(self, x, y, index, canvas_name, color=(59, 112, 219)):
        self.is_selected = None
        self.canvas = None
        r = 8
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.x = x
        self.y = y
        self.r = r
        self.index = index
        self.canvas_name = canvas_name
        self.color = color

        self.oval = canvas_name.create_oval(
            x0, y0, x1, y1, fill="#%02x%02x%02x" % self.color, tags="node"
        )
        self.edges = []  # Список всех ребер, соединенных с этим узлом

        # self.text_item = canvas_name.create_text(
        #     x, y,
        #     text=f"{self.index}",
        #     fill="white",
        #     font=("Arial", 8)  # Шрифт и размер текста
        # )

    def select(self):
        self.is_selected = True
        self.canvas_name.itemconfig(self.oval, fill="black")

    def deselect(self):
        self.is_selected = False
        self.canvas_name.itemconfig(self.oval, fill="#%02x%02x%02x" % self.color)

    def is_inside(self, x1, y1, x2, y2):
        return x1 <= self.x <= x2 and y1 <= self.y <= y2

    def clicked_up(self):
        # convert to RGB
        self.canvas_name.itemconfig(self.oval, fill="#%02x%02x%02x" % self.color)

    def is_collide(self, x, y):
        return ((x - self.x) ** 2 + (y - self.y) ** 2) < (self.r * 2) ** 2

    def is_clicked(self, x, y):
        return ((x - self.x) ** 2 + (y - self.y) ** 2) < self.r**2

    def update_edges(self):
        for edge in self.edges:
            edge.update_position()

    def update_node(self, x, y):
        self.x = x
        self.y = y
        self.canvas_name.coords(
            self.oval, x - self.r, y - self.r, x + self.r, y + self.r
        )

    def delete(self):
        if self.is_selected:
            self.canvas_name.delete(self.oval)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        elif type(other) is tuple:
            return self.x == other[0] and self.y == other[1]
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    # def __del__(self):
    #     if self.is_selected:
    #         self.canvas_name.delete(self.oval)
