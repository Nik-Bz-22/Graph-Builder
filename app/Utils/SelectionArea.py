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
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="black"
        )

    def on_mouse_drag(self, event):
        """Обновление прямоугольника выделения при перетаскивании."""
        cur_x, cur_y = event.x, event.y
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