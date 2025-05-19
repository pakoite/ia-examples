import tkinter as tk
import heapq
import time
import threading

# Definir grafo con posiciones de los nodos (para visualización)
nodes = {
    "A": (100, 100),
    "B": (300, 100),
    "C": (500, 100),
    "D": (200, 250),
    "E": (400, 250),
    "F": (300, 400),
}

# Grafo como diccionario de adyacencia con pesos
graph = {
    "A": {"B": 2, "D": 4},
    "B": {"A": 2, "C": 3, "E": 1},
    "C": {"B": 3, "E": 2},
    "D": {"A": 4, "E": 3, "F": 6},
    "E": {"B": 1, "C": 2, "D": 3, "F": 1},
    "F": {"D": 6, "E": 1},
}

start_node = "A"
end_node = "F"
visited_nodes = set()
path_result = []

# Crear ventana
root = tk.Tk()
root.title("Dijkstra Visual")
canvas = tk.Canvas(root, width=600, height=500, bg="white")
canvas.pack()


def draw_graph(highlight_path=[], explored=set()):
    canvas.delete("all")
    # Dibujar aristas
    for node, edges in graph.items():
        x1, y1 = nodes[node]
        for neighbor, weight in edges.items():
            x2, y2 = nodes[neighbor]
            color = (
                "orange"
                if (node, neighbor) in highlight_path
                or (neighbor, node) in highlight_path
                else "gray"
            )
            canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            canvas.create_text(
                mid_x, mid_y, text=str(weight), fill="black", font=("Arial", 10)
            )

    # Dibujar nodos
    for node, (x, y) in nodes.items():
        fill = (
            "green"
            if node == start_node
            else (
                "red"
                if node == end_node
                else "lightblue" if node in explored else "white"
            )
        )
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill, outline="black")
        canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))


def dijkstra(start, end):
    global visited_nodes, path_result
    visited_nodes = set()
    path_result = []

    dist = {node: float("inf") for node in graph}
    prev = {}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)
        if current in visited_nodes:
            continue
        visited_nodes.add(current)

        draw_graph(explored=visited_nodes)
        time.sleep(0.5)

        if current == end:
            break

        for neighbor, weight in graph[current].items():
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    # Reconstruir camino
    path = []
    current = end
    while current in prev:
        path.append((current, prev[current]))
        current = prev[current]
    path_result = path

    draw_graph(highlight_path=path_result, explored=visited_nodes)


def start_dijkstra():
    threading.Thread(target=dijkstra, args=(start_node, end_node), daemon=True).start()


# Botón para comenzar
btn = tk.Button(root, text="Iniciar Dijkstra", command=start_dijkstra)
btn.pack(pady=10)

draw_graph()
root.mainloop()
