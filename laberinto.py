import tkinter as tk
import random

# Parámetros
TILE_SIZE = 30
ROWS, COLS = 21, 21  # Impares para permitir muros entre celdas

# Crear ventana
root = tk.Tk()
root.title("Laberinto Aleatorio con Tkinter")
canvas = tk.Canvas(root, width=COLS * TILE_SIZE, height=ROWS * TILE_SIZE, bg="white")
canvas.pack()

# Inicializar laberinto: 1 = muro, 0 = camino
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
player_pos = [1, 1]  # Comienzo
meta = [ROWS - 2, COLS - 2]  # Final


# Generador recursivo de laberinto
def generar_laberinto(x=1, y=1):
    dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(dirs)
    maze[x][y] = 0
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 1 <= nx < ROWS - 1 and 1 <= ny < COLS - 1 and maze[nx][ny] == 1:
            maze[x + dx // 2][y + dy // 2] = 0  # Abrir paso
            generar_laberinto(nx, ny)


# Dibujo del laberinto y jugador
def draw_maze():
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            color = "black" if maze[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * TILE_SIZE,
                i * TILE_SIZE,
                (j + 1) * TILE_SIZE,
                (i + 1) * TILE_SIZE,
                fill=color,
                outline="gray",
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


# Movimiento del jugador
def move(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < ROWS and 0 <= new_y < COLS:
        if maze[new_x][new_y] == 0:
            player_pos[0] = new_x
            player_pos[1] = new_y
            draw_maze()
            if player_pos == meta:
                canvas.create_text(
                    COLS * TILE_SIZE // 2,
                    ROWS * TILE_SIZE // 2,
                    text="¡Ganaste!",
                    font=("Arial", 24),
                    fill="red",
                )


# Captura teclas
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


# Inicialización
generar_laberinto()
maze[meta[0]][meta[1]] = 0  # Asegurar acceso a la meta
draw_maze()
root.bind("<Key>", on_key)
root.mainloop()
