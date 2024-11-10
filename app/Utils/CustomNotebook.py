import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab and background image support"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not CustomNotebook.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        super().__init__(*args, **kwargs)

        self._active = None
        self._background_images = {}  # Dictionary to store background images

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(["pressed"])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(["pressed"]):
            return
        element = self.identify(event.x, event.y)
        if "close" not in element:
            return
        index = self.index("@%d,%d" % (event.x, event.y))
        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")
        self.state(["!pressed"])
        self._active = None

    def set_background(self, tab_index, image_path):
        """Set background image for a specific tab"""
        image = Image.open(image_path)
        bg_image = ImageTk.PhotoImage(image)
        tab_canvas = self.nametowidget(self.tabs()[tab_index])

        # Display the background image on the specified tab
        tab_canvas.create_image(0, 0, anchor="nw", image=bg_image)

        # Store the reference to the image to prevent garbage collection
        self._background_images[tab_index] = bg_image

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage(
                "img_close",
                data="""
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                """,
            ),
            tk.PhotoImage(
                "img_closeactive",
                data="""
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                """,
            ),
            tk.PhotoImage(
                "img_closepressed",
                data="""
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                """,
            ),
        )

        style.element_create(
            "close",
            "image",
            "img_close",
            ("active", "pressed", "!disabled", "img_closepressed"),
            ("active", "!disabled", "img_closeactive"),
            border=8,
            sticky="",
        )

        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout(
            "CustomNotebook.Tab",
            [
                (
                    "CustomNotebook.tab",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "CustomNotebook.padding",
                                {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "CustomNotebook.focus",
                                            {
                                                "side": "top",
                                                "sticky": "nswe",
                                                "children": [
                                                    (
                                                        "CustomNotebook.label",
                                                        {"side": "left", "sticky": ""},
                                                    ),
                                                    (
                                                        "CustomNotebook.close",
                                                        {"side": "left", "sticky": ""},
                                                    ),
                                                ],
                                            },
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
