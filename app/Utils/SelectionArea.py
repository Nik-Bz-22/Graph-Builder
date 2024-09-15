class SelectionArea:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect_id = None
        self.start_x = None
        self.start_y = None
        self.nodes = []

    def on_mouse_down_s(self, event):
        try:
            item_id = self.canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)[0]
            if not self.canvas.gettags(item_id) == ("node",):
                return
            # if "node" in self.canvas.gettags(item_id):
            #     print("noda tyt", item_id)
            #     return
        except IndexError as er:
            pass

        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="black"
        )

    def on_mouse_drag(self, event):
        if self.rect_id:
            cur_x, cur_y = event.x, event.y
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)
        else:
            # print("error")
            pass
    def on_mouse_release(self, event):
        if not self.rect_id:
            return
        end_x, end_y = event.x, event.y

        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        for node in self.nodes:
            if node.is_inside(x1, y1, x2, y2):
                node.select()
            else:
                node.deselect()

        self.canvas.delete(self.rect_id)
        self.rect_id = None
