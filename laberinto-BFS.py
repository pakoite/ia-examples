import tkinter as tk
import random
import time
import threading
from collections import deque

# Parámetros
TILE_SIZE = 30
ROWS, COLS = 21, 21  # Impares para tener muros

root = tk.Tk()
root.title("Laberinto BFS Animado")
canvas = tk.Canvas(root, width=COLS * TILE_SIZE, height=ROWS * TILE_SIZE, bg="white")
canvas.pack()

maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
player_pos = [1, 1]
meta = [ROWS - 2, COLS - 2]
visitados = set()
camino_bfs = []


def generar_laberinto(x=1, y=1):
    dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(dirs)
    maze[x][y] = 0
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 1 <= nx < ROWS - 1 and 1 <= ny < COLS - 1 and maze[nx][ny] == 1:
            maze[x + dx // 2][y + dy // 2] = 0
            generar_laberinto(nx, ny)


def draw_maze(path=[], explored=set()):
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            if (i, j) in explored:
                color = "lightblue"
            else:
                color = "black" if maze[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * TILE_SIZE,
                i * TILE_SIZE,
                (j + 1) * TILE_SIZE,
                (i + 1) * TILE_SIZE,
                fill=color,
                outline="gray",
            )
    for x, y in path:
        canvas.create_rectangle(
            y * TILE_SIZE + 8,
            x * TILE_SIZE + 8,
            (y + 1) * TILE_SIZE - 8,
            (x + 1) * TILE_SIZE - 8,
            fill="yellow",
        )
    # Meta
    m_x, m_y = meta
    canvas.create_rectangle(
        m_y * TILE_SIZE,
        m_x * TILE_SIZE,
        (m_y + 1) * TILE_SIZE,
        (m_x + 1) * TILE_SIZE,
        fill="green",
    )
    # Jugador
    x, y = player_pos
    canvas.create_rectangle(
        y * TILE_SIZE,
        x * TILE_SIZE,
        (y + 1) * TILE_SIZE,
        (x + 1) * TILE_SIZE,
        fill="blue",
    )


def move(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < ROWS and 0 <= new_y < COLS:
        if maze[new_x][new_y] == 0:
            player_pos[0] = new_x
            player_pos[1] = new_y
            draw_maze(camino_bfs, visitados)
            if player_pos == meta:
                canvas.create_text(
                    COLS * TILE_SIZE // 2,
                    ROWS * TILE_SIZE // 2,
                    text="¡Ganaste!",
                    font=("Arial", 24),
                    fill="red",
                )


def on_key(event):
    key = event.keysym
    if key == "Up":
        move(-1, 0)
    elif key == "Down":
        move(1, 0)
    elif key == "Left":
        move(0, -1)
    elif key == "Right":
        move(0, 1)
    elif key == "s":
        threading.Thread(target=resolver_bfs, daemon=True).start()


def resolver_bfs():
    global camino_bfs, visitados
    visitados = set()
    came_from = {}
    queue = deque()
    start = tuple(player_pos)
    goal = tuple(meta)
    queue.append(start)
    visitados.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                neighbor = (nx, ny)
                if neighbor not in visitados:
                    visitados.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        draw_maze([], visitados)
        time.sleep(0.01)

    # Reconstruir camino
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return  # Sin solución
    path.reverse()
    camino_bfs = path

    # Animar el recorrido
    for step in path:
        time.sleep(0.05)
        player_pos[0], player_pos[1] = step
        draw_maze(path, visitados)

    canvas.create_text(
        COLS * TILE_SIZE // 2,
        ROWS * TILE_SIZE // 2,
        text="¡Resuelto!",
        font=("Arial", 24),
        fill="red",
    )


# Inicializar
generar_laberinto()
maze[meta[0]][meta[1]] = 0
draw_maze()
root.bind("<Key>", on_key)
root.mainloop()
