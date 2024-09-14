import json
from tkinter import filedialog
from .paths import ROOT_DIR


class FileManager:
    @staticmethod
    def write_json_with_pos(
        graph: list[tuple[float, tuple[int, int], tuple[int, int]]],
        filepath="dataGraph.json",
    ):
        if len(graph) < 1:
            return
        with open(filepath, "w") as file:
            json.dump(graph, file, indent=4)

    @staticmethod
    def read_json_with_pos(filepath="dataGraph.json"):
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def write_to_txt(
        graph: list[tuple[float, tuple[int, int], tuple[int, int]]],
        filepath="dataGraph.txt",
    ):
        with open(filepath, "w") as file:
            for edge in graph:
                file.write(
                    f"{edge[0]} {edge[1][0]} {edge[1][1]} {edge[2][0]} {edge[2][1]}\n"
                )

    @staticmethod
    def read_txt_with_pos(filepath="dataGraph.txt"):
        data = []
        with open(filepath, "r") as file:
            text = file.read().strip().split("\n")
            for i in text:
                row = i.split(" ")
                # print(row)
                data.append(
                    (
                        float(row[0]),
                        (int(row[1]), int(row[2])),
                        (int(row[3]), int(row[4])),
                    )
                )

        return data

    def save_as(self, graph):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            try:
                self.write_to_txt(graph, file_path)
                print(f"File saved: {file_path}")
                return file_path

            except Exception as e:
                print(f"Error saving file: {e}")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                graph = self.read_txt_with_pos(file_path)
                print(f"File open: {file_path}")
                return {"graph": graph, "filepath": file_path}

            except Exception as e:
                print(f"Error opening file: {e}")


if __name__ == "__main__":
    f = FileManager()
    f.read_txt_with_pos(filepath=ROOT_DIR / "dataGraph.txt")
