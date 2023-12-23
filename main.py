import tkinter as tk
import random

class JeuDeLaVie:
    def __init__(self, root, rows, cols, cell_size=20):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.generation = 0
        self.colors_used = []

        # Création de la grille
        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

        # Création du canvas
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack()

        # Label pour afficher le numéro de génération
        self.gen_label = tk.Label(root, text=f"Génération : {self.generation}", font=("Helvetica", 12), bg="white")
        self.gen_label.pack(pady=5)

        # Ajout d'un bouton pour démarrer/arrêter la simulation
        self.start_button = tk.Button(root, text="Start/Stop", command=self.toggle_simulation, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)

        # Initialisation de la simulation
        self.is_running = False
        self.update()

    def toggle_simulation(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.config(text="Pause", bg="#FF5733")
            self.update()
        else:
            self.start_button.config(text="Start", bg="#4CAF50")

    def update(self):
        if self.is_running:
            self.evolve()
        self.draw()
        self.root.after(100, self.update)  # Met à jour toutes les 100 millisecondes

    def evolve(self):
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1

        self.grid = new_grid
        self.generation += 1

    def count_neighbors(self, i, j):
        neighbors = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    neighbors += self.grid[ni][nj]
        neighbors -= self.grid[i][j]
        return neighbors

    def draw(self):
        self.canvas.delete("all")

        current_color = self.get_unique_color()
        for i in range(self.rows):
            for j in range(self.cols):
                x, y = j * self.cell_size, i * self.cell_size
                color = current_color if self.grid[i][j] == 1 else "white"
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color, outline="#ccc")

        self.gen_label.config(text=f"Génération : {self.generation}", fg=current_color)

    def get_unique_color(self):
        color_options = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "pink"]
        available_colors = [color for color in color_options if color not in self.colors_used]

        if not available_colors:
            # Si toutes les couleurs sont déjà utilisées, réinitialiser la liste des couleurs utilisées
            self.colors_used = []

        color = random.choice(available_colors)
        self.colors_used.append(color)

        return color

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mini-Jeu de la Vie")
    root.configure(bg="white")
    
    jeu = JeuDeLaVie(root, rows=30, cols=30)
    
    root.mainloop()
