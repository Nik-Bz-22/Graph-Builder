import tkinter as tk
from tkinter import simpledialog


class Edge:
    def __init__(self, node1, node2, canvas_name, weight=0):
        self.node1 = node1
        self.node2 = node2
        self.canvas_name = canvas_name
        self.weight = weight
        self.line = canvas_name.create_line(
            node1.x, node1.y, node2.x, node2.y, arrow=tk.LAST, width=2
        )
        self.text = canvas_name.create_text(
            (node1.x + node2.x) // 2,
            (node1.y + node2.y) // 2,
            text=f"{self.weight}",
            fill="black",
            font=("Arial", 16),
        )
        node1.edges.append(self)
        node2.edges.append(self)

        self.canvas_name.tag_bind(self.text, "<Double-1>", self.change_weight)

    def update_position(self):
        self.canvas_name.coords(
            self.line, self.node1.x, self.node1.y, self.node2.x, self.node2.y
        )
        self.canvas_name.coords(
            self.text,
            (self.node1.x + self.node2.x) // 2,
            (self.node1.y + self.node2.y) // 2,
        )

    def change_weight(self, event):
        new_weight = simpledialog.askfloat(
            "Input", "Enter the new edge's weight:", minvalue=0, maxvalue=100
        )
        if new_weight is not None:
            self.weight = new_weight
            self.canvas_name.itemconfig(self.text, text=str(self.weight))

    def delete(self):
        self.canvas_name.delete(self.line)
        self.canvas_name.delete(self.text)
