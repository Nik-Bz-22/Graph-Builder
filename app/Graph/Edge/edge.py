import tkinter as tk
from tkinter import simpledialog


class Edge:

    def __init__(self, node1, node2, canvas_name, weight=0):
        self.node1 = node1
        self.node2 = node2
        self.canvas_name = canvas_name
        self.weight = weight  # Вес ребра по умолчанию 0
        # Создаем линию
        self.line = canvas_name.create_line(node1.x, node1.y, node2.x, node2.y, arrow=tk.LAST, width=2)
        # Текст для отображения веса ребра
        self.text = canvas_name.create_text(
            (node1.x + node2.x) // 2,
            (node1.y + node2.y) // 2,
            text=f"{self.weight}",
            fill="black",
            font=("Arial", 16)


        )
        # Добавляем ребро в список ребер обоих узлов
        node1.edges.append(self)
        node2.edges.append(self)

        # Добавляем обработчик для двойного клика по весу ребра
        self.canvas_name.tag_bind(self.text, "<Double-1>", self.change_weight)

    def update_position(self):
        """Обновляет положение линии в соответствии с положением узлов"""
        self.canvas_name.coords(self.line, self.node1.x, self.node1.y, self.node2.x, self.node2.y)
        # Обновляем позицию текста с весом ребра
        self.canvas_name.coords(
            self.text,
            (self.node1.x + self.node2.x) // 2,
            (self.node1.y + self.node2.y) // 2
        )


    def change_weight(self, event):
        """Изменение веса ребра по двойному клику"""
        new_weight = simpledialog.askfloat("Input", "Введите новый вес ребра:", minvalue=0, maxvalue=100)
        if new_weight is not None:
            self.weight = new_weight
            self.canvas_name.itemconfig(self.text, text=str(self.weight))

    def delete(self):
        # Удаляем линию с холста
        self.canvas_name.delete(self.line)
        self.canvas_name.delete(self.text)


