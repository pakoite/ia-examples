import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq
import time
import threading
import math


class GraphVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Visualizador de Grafos - Dijkstra y A*")

        self.canvas = tk.Canvas(master, width=700, height=500, bg="white")
        self.canvas.pack()

        self.nodes = {}  # nodo: (x, y)
        self.graph = {}  # nodo: {vecino: peso}
        self.node_radius = 20

        self.start_node = None
        self.end_node = None

        self.visited_nodes = set()
        self.path_result = []

        self.mode = "dijkstra"  # o "astar"

        # UI botones
        frame = tk.Frame(master)
        frame.pack(pady=5)

        self.btn_add_node = tk.Button(
            frame, text="Agregar Nodo", command=self.add_node_prompt
        )
        self.btn_add_node.grid(row=0, column=0)

        self.btn_add_edge = tk.Button(
            frame, text="Agregar Arista", command=self.add_edge_prompt
        )
        self.btn_add_edge.grid(row=0, column=1)

        self.btn_set_start = tk.Button(
            frame, text="Definir Inicio", command=self.set_start_prompt
        )
        self.btn_set_start.grid(row=0, column=2)

        self.btn_set_end = tk.Button(
            frame, text="Definir Fin", command=self.set_end_prompt
        )
        self.btn_set_end.grid(row=0, column=3)

        self.btn_algo = tk.Button(frame, text="Usar A*", command=self.toggle_algorithm)
        self.btn_algo.grid(row=0, column=4)

        self.btn_run = tk.Button(frame, text="Ejecutar", command=self.run_algorithm)
        self.btn_run.grid(row=0, column=5)

        self.canvas.bind("<Button-1>", self.click_canvas)

        self.temp_new_node_pos = None  # para colocar nodo en canvas

        self.draw_graph()

    def add_node_prompt(self):
        name = simpledialog.askstring("Nodo", "Nombre del nodo (único):")
        if not name:
            return
        if name in self.nodes:
            messagebox.showerror("Error", "Nodo ya existe")
            return
        messagebox.showinfo(
            "Info", f"Haz click en el canvas para colocar nodo '{name}'"
        )
        self.temp_new_node_pos = name

    def add_edge_prompt(self):
        if len(self.nodes) < 2:
            messagebox.showerror("Error", "Necesitas al menos 2 nodos")
            return
        node1 = simpledialog.askstring("Arista", "Nodo origen:")
        node2 = simpledialog.askstring("Arista", "Nodo destino:")
        if node1 not in self.nodes or node2 not in self.nodes:
            messagebox.showerror("Error", "Nodo(s) no existen")
            return
        try:
            peso = float(simpledialog.askstring("Arista", "Peso (número positivo):"))
            if peso <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Peso inválido")
            return
        # Grafo no dirigido
        self.graph.setdefault(node1, {})[node2] = peso
        self.graph.setdefault(node2, {})[node1] = peso
        self.draw_graph()

    def set_start_prompt(self):
        node = simpledialog.askstring("Inicio", "Nodo inicio:")
        if node not in self.nodes:
            messagebox.showerror("Error", "Nodo no existe")
            return
        self.start_node = node
        self.draw_graph()

    def set_end_prompt(self):
        node = simpledialog.askstring("Fin", "Nodo fin:")
        if node not in self.nodes:
            messagebox.showerror("Error", "Nodo no existe")
            return
        self.end_node = node
        self.draw_graph()

    def toggle_algorithm(self):
        if self.mode == "dijkstra":
            self.mode = "astar"
            self.btn_algo.config(text="Usar Dijkstra")
        else:
            self.mode = "dijkstra"
            self.btn_algo.config(text="Usar A*")

    def click_canvas(self, event):
        if self.temp_new_node_pos:
            name = self.temp_new_node_pos
            self.nodes[name] = (event.x, event.y)
            if name not in self.graph:
                self.graph[name] = {}
            self.temp_new_node_pos = None
            self.draw_graph()

    def draw_graph(self, highlight_path=[], explored=set()):
        self.canvas.delete("all")
        # Dibujar aristas
        for node, edges in self.graph.items():
            x1, y1 = self.nodes[node]
            for neighbor, weight in edges.items():
                x2, y2 = self.nodes[neighbor]
                color = (
                    "orange"
                    if (node, neighbor) in highlight_path
                    or (neighbor, node) in highlight_path
                    else "gray"
                )
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_text(
                    mid_x,
                    mid_y,
                    text=str(round(weight, 2)),
                    fill="black",
                    font=("Arial", 10),
                )

        # Dibujar nodos
        for node, (x, y) in self.nodes.items():
            if node == self.start_node:
                fill = "green"
            elif node == self.end_node:
                fill = "red"
            elif node in explored:
                fill = "lightblue"
            else:
                fill = "white"
            self.canvas.create_oval(
                x - self.node_radius,
                y - self.node_radius,
                x + self.node_radius,
                y + self.node_radius,
                fill=fill,
                outline="black",
            )
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

    def run_algorithm(self):
        if not self.start_node or not self.end_node:
            messagebox.showerror("Error", "Define nodo inicio y fin primero")
            return
        threading.Thread(target=self._run, daemon=True).start()

    def heuristic(self, node):
        # Heurística Euclidiana para A*
        x1, y1 = self.nodes[node]
        x2, y2 = self.nodes[self.end_node]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def _run(self):
        self.visited_nodes = set()
        self.path_result = []

        dist = {node: float("inf") for node in self.nodes}
        prev = {}
        dist[self.start_node] = 0

        heap = []
        if self.mode == "dijkstra":
            heapq.heappush(heap, (0, self.start_node))
        else:  # A*
            heapq.heappush(heap, (0 + self.heuristic(self.start_node), self.start_node))

        while heap:
            current_f, current = heapq.heappop(heap)
            if current in self.visited_nodes:
                continue
            self.visited_nodes.add(current)

            self.draw_graph(explored=self.visited_nodes)
            time.sleep(0.5)

            if current == self.end_node:
                break

            for neighbor, peso in self.graph.get(current, {}).items():
                tentative_g = dist[current] + peso
                if tentative_g < dist[neighbor]:
                    dist[neighbor] = tentative_g
                    prev[neighbor] = current
                    f = tentative_g
                    if self.mode == "astar":
                        f += self.heuristic(neighbor)
                    heapq.heappush(heap, (f, neighbor))

        # Reconstruir camino
        path = []
        current = self.end_node
        while current in prev:
            path.append((current, prev[current]))
            current = prev[current]
        self.path_result = path

        self.draw_graph(highlight_path=self.path_result, explored=self.visited_nodes)

        messagebox.showinfo("Resultado", f"Ruta encontrada con {self.mode.upper()}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()
