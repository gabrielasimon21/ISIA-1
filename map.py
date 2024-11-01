import spade
import tkinter as tk
import random
from PIL import ImageGrab
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio


class Map:
    def __init__(self):
        self.GRID_SIZE = 20
        self.CELL_SIZE = 30
        self.fenomeno = random.choice(("Terramoto", "Terramoto + Tsunami", "Tsunami"))
        self.population_data = [[66, 117, 80, 149, 140, 54, 145, 21, 132, 51, 140, 25, 135, 122, 27, 34, 65, 90, 156, 98], [130, 126, 93, 57, 144, 152, 62, 54, 26, 139, 22, 152, 65, 78, 35, 101, 139, 149, 146, 145], [135, 15, 100, 105, 124, 157, 106, 45, 111, 120, 151, 98, 58, 52, 34, 92, 42, 140, 97, 23], [44, 125, 138, 103, 29, 30, 141, 84, 49, 32, 147, 66, 33, 26, 37, 102, 146, 134, 160, 107], [122, 154, 111, 32, 125, 106, 97, 21, 63, 88, 111, 106, 75, 19, 93, 138, 156, 108, 80, 88], [76, 83, 142, 120, 39, 139, 154, 48, 122, 63, 50, 79, 117, 116, 99, 101, 103, 47, 39, 103], [158, 61, 123, 70, 140, 67, 149, 94, 70, 27, 136, 113, 147, 94, 132, 129, 68, 149, 58, 103], [110, 45, 30, 98, 150, 19, 83, 75, 83, 69, 84, 53, 86, 102, 81, 69, 134, 48, 99, 79], [91, 106, 115, 82, 152, 141, 56, 24, 109, 53, 130, 83, 129, 150, 21, 124, 63, 147, 34, 49], [54, 25, 143, 27, 109, 137, 57, 126, 156, 160, 155, 39, 156, 102, 114, 46, 18, 119, 108, 61], [95, 98, 27, 136, 143, 37, 148, 148, 92, 50, 103, 96, 51, 71, 38, 151, 160, 87, 144, 45], [157, 62, 18, 75, 52, 45, 69, 83, 133, 24, 149, 91, 101, 153, 136, 73, 152, 89, 52, 130], [63, 88, 156, 76, 153, 135, 128, 90, 154, 69, 63, 99, 70, 27, 51, 102, 129, 119, 127, 133], [140, 61, 134, 64, 58, 40, 141, 160, 143, 150, 107, 93, 113, 22, 15, 85, 58, 54, 123, 106], [24, 59, 148, 103, 69, 116, 157, 51, 108, 143, 47, 26, 20, 117, 37, 94, 16, 43, 155, 85], [84, 135, 23, 54, 122, 114, 105, 68, 21, 16, 99, 114, 59, 104, 99, 149, 48, 60, 46, 132], [69, 88, 27, 89, 137, 47, 120, 94, 90, 152, 153, 22, 82, 132, 34, 25, 34, 129, 61, 46], [105, 44, 19, 108, 107, 148, 97, 67, 34, 84, 24, 77, 52, 120, 101, 96, 115, 75, 108, 46], [98, 81, 155, 142, 20, 27, 122, 82, 43, 0, 0, 0, 148, 158, 58, 116, 127, 99, 29, 51], [91, 99, 57, 82, 124, 141, 137, 48, 0, 0, 0, 0, 0, 0, 77, 88, 17, 120, 43, 140]]
        self.road_points = [(7, 17, 7, 15), (7, 16, 7, 15), (7, 15, 7, 15), (18, 13, 7, 13), (17, 13, 7, 13),
                       (16, 13, 7, 13), (15, 13, 7, 13), (14, 13, 7, 13), (13, 13, 7, 13), (12, 13, 7, 13),
                       (11, 13, 7, 13), (10, 13, 7, 13), (9, 13, 7, 13), (8, 13, 7, 13), (7, 13, 7, 13), (17, 9, 7, 9),
                       (16, 9, 7, 9), (15, 9, 7, 9), (14, 9, 7, 9), (13, 9, 7, 9), (12, 9, 7, 9), (11, 9, 7, 9),
                       (10, 9, 7, 9), (9, 9, 7, 9), (8, 9, 7, 9), (7, 9, 7, 9), (17, 1, 17, 7), (17, 2, 17, 7),
                       (17, 3, 17, 7), (17, 4, 17, 7), (17, 5, 17, 7), (17, 6, 17, 7), (17, 7, 17, 7), (5, 1, 5, 19),
                       (5, 2, 5, 19), (5, 3, 5, 19), (5, 4, 5, 19), (5, 5, 5, 19), (5, 6, 5, 19), (5, 7, 5, 19),
                       (5, 8, 5, 19), (5, 9, 5, 19), (5, 10, 5, 19), (5, 11, 5, 19), (5, 12, 5, 19), (5, 13, 5, 19),
                       (5, 14, 5, 19), (5, 15, 5, 19), (5, 16, 5, 19), (5, 17, 5, 19), (5, 18, 5, 19), (5, 19, 5, 19),
                       (19, 19, 19, 17), (19, 18, 19, 17), (19, 17, 19, 17), (17, 7, 19, 7), (18, 7, 19, 7),
                       (19, 7, 19, 7), (18, 15, 18, 13), (18, 14, 18, 13), (18, 13, 18, 13), (1, 1, 1, 19),
                       (1, 2, 1, 19), (1, 3, 1, 19), (1, 4, 1, 19), (1, 5, 1, 19), (1, 6, 1, 19), (1, 7, 1, 19),
                       (1, 8, 1, 19), (1, 9, 1, 19), (1, 10, 1, 19), (1, 11, 1, 19), (1, 12, 1, 19), (1, 13, 1, 19),
                       (1, 14, 1, 19), (1, 15, 1, 19), (1, 16, 1, 19), (1, 17, 1, 19), (1, 18, 1, 19), (1, 19, 1, 19),
                       (7, 11, 17, 11), (8, 11, 17, 11), (9, 11, 17, 11), (10, 11, 17, 11), (11, 11, 17, 11),
                       (12, 11, 17, 11), (13, 11, 17, 11), (14, 11, 17, 11), (15, 11, 17, 11), (16, 11, 17, 11),
                       (17, 11, 17, 11), (11, 1, 13, 1), (12, 1, 13, 1), (13, 1, 13, 1), (13, 7, 15, 7), (14, 7, 15, 7),
                       (15, 7, 15, 7), (19, 7, 19, 1), (19, 6, 19, 1), (19, 5, 19, 1), (19, 4, 19, 1), (19, 3, 19, 1),
                       (19, 2, 19, 1), (19, 1, 19, 1), (19, 17, 7, 17), (18, 17, 7, 17), (17, 17, 7, 17),
                       (16, 17, 7, 17), (15, 17, 7, 17), (14, 17, 7, 17), (13, 17, 7, 17), (12, 17, 7, 17),
                       (11, 17, 7, 17), (10, 17, 7, 17), (9, 17, 7, 17), (8, 17, 7, 17), (7, 17, 7, 17),
                       (5, 19, 19, 19), (6, 19, 19, 19), (7, 19, 19, 19), (8, 19, 19, 19), (9, 19, 19, 19),
                       (10, 19, 19, 19), (11, 19, 19, 19), (12, 19, 19, 19), (13, 19, 19, 19), (14, 19, 19, 19),
                       (15, 19, 19, 19), (16, 19, 19, 19), (17, 19, 19, 19), (18, 19, 19, 19), (19, 19, 19, 19),
                       (17, 11, 17, 9), (17, 10, 17, 9), (17, 9, 17, 9), (7, 9, 7, 1), (7, 8, 7, 1), (7, 7, 7, 1),
                       (7, 6, 7, 1), (7, 5, 7, 1), (7, 4, 7, 1), (7, 3, 7, 1), (7, 2, 7, 1), (7, 1, 7, 1),
                       (13, 1, 13, 7), (13, 2, 13, 7), (13, 3, 13, 7), (13, 4, 13, 7), (13, 5, 13, 7), (13, 6, 13, 7),
                       (13, 7, 13, 7), (9, 7, 11, 7), (10, 7, 11, 7), (11, 7, 11, 7), (7, 1, 9, 1), (8, 1, 9, 1),
                       (9, 1, 9, 1), (9, 1, 9, 7), (9, 2, 9, 7), (9, 3, 9, 7), (9, 4, 9, 7), (9, 5, 9, 7), (9, 6, 9, 7),
                       (9, 7, 9, 7), (7, 15, 19, 15), (8, 15, 19, 15), (9, 15, 19, 15), (10, 15, 19, 15),
                       (11, 15, 19, 15), (12, 15, 19, 15), (13, 15, 19, 15), (14, 15, 19, 15), (15, 15, 19, 15),
                       (16, 15, 19, 15), (17, 15, 19, 15), (18, 15, 19, 15), (19, 15, 19, 15), (3, 1, 5, 1),
                       (4, 1, 5, 1), (5, 1, 5, 1), (15, 7, 15, 1), (15, 6, 15, 1), (15, 5, 15, 1), (15, 4, 15, 1),
                       (15, 3, 15, 1), (15, 2, 15, 1), (15, 1, 15, 1), (1, 19, 3, 19), (2, 19, 3, 19), (3, 19, 3, 19),
                       (11, 7, 11, 1), (11, 6, 11, 1), (11, 5, 11, 1), (11, 4, 11, 1), (11, 3, 11, 1), (11, 2, 11, 1),
                       (11, 1, 11, 1), (15, 1, 17, 1), (16, 1, 17, 1), (17, 1, 17, 1), (3, 19, 3, 1), (3, 18, 3, 1),
                       (3, 17, 3, 1), (3, 16, 3, 1), (3, 15, 3, 1), (3, 14, 3, 1), (3, 13, 3, 1), (3, 12, 3, 1),
                       (3, 11, 3, 1), (3, 10, 3, 1), (3, 9, 3, 1), (3, 8, 3, 1), (3, 7, 3, 1), (3, 6, 3, 1),
                       (3, 5, 3, 1), (3, 4, 3, 1), (3, 3, 3, 1), (3, 2, 3, 1), (3, 1, 3, 1), (7, 9, 15, 9),
                       (8, 9, 15, 9), (9, 9, 15, 9), (10, 9, 15, 9), (11, 9, 15, 9), (12, 9, 15, 9), (13, 9, 15, 9),
                       (14, 9, 15, 9), (15, 9, 15, 9), (7, 13, 7, 11), (7, 12, 7, 11), (7, 11, 7, 11)]
        self.points =  {(18, 4): 'black', (15, 14): 'black', (18, 20): 'magenta', (10, 8): 'magenta', (2, 8): 'magenta',
              (9, 12): 'red', (17, 6): 'red', (3, 3): 'red', (6, 17): 'red', (4, 6): 'red', (17, 15): 'red'}
        self.sea_points = [( 18 , 9 ) , ( 18 , 10 ) , ( 18 , 11 ) , ( 19 , 8 ) , ( 19 , 9 ) , ( 19 , 10 ) , ( 19 , 11 ) , ( 19 , 12 ) , ( 19 , 13 ) ]
        self.informations = {}
        for i in range(20):
            for j in range(20):
                key = (i, j)
                value = [0 for _ in range(3)]
                self.informations[key] = value
        #Dicionário: 1º valor - nº de mortos, 2º valor - nº de feridos, 3º valor - nº de mortos resgatados, 4º valor - nº de feridos resgatados
        self.affected_services = [[0 for _ in range(50)] for _ in range(50)]
        self.root = tk.Tk()
        self.root2 = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.frame, width=900, height=600)
        self.legend_frame = tk.Frame(self.root)
        self.legend_colors_earthquake = [0] * 30
        self.legend_intensity_earthquake = [0] * 30
        self.legend_colors_tsunami = [0] * 30
        self.legend_intensity_tsunami = [0] * 30
        self.n_mortos = 0
        self.n_feridos = 0
        self.n_civis_abrigo = 0
        self.dados = [0] * 6
        self.descricoes = ["Nº de mortos: ", "Nº de feridos: ", "Nº Responders (bases) destruídos: ",
                      "Nº de Shelters destruídos: ", "Nº de Supply (bases) destruídas: ", "Nº de civis precisam abrigo: "]
        self.affected_points = [[0 for _ in range (20)] for _ in range (20)]

        self.label_valor_mortos = None
        self.label_valor_feridos = None

    async def setup(self):
        self.create_gui()

    # Função que inicia a interface gráfica
    def create_gui(self):
        self.root.title(f"Mapa Cidade: {self.fenomeno}")
        self.root2.title("Dados de destruição")
        self.frame.grid(column=0, row=0, padx=10, pady=10)
        self.canvas.grid(row=0, column=0)
        self.legendas()
        if self.fenomeno == "Terramoto":
            self.terramoto()
        elif self.fenomeno == "Tsunami":
            self.tsunami()
        else:
            self.terramoto_tsunami()
        self.legendas2()
        self.draw_road()
        self.draw_points()
        # Exibir uma mensagem (ou imagem estática)
        save_button = tk.Button(self.root, command=lambda: self.save_and_close(self.root, 1))
        save_button.grid(row=1, column=0, padx=10, pady=10)
        save_button2 = tk.Button(self.root2, command=lambda: self.save_and_close(self.root2, 2))
        save_button2.grid(row=1, column=0, padx=10, pady=10)
        self.root.mainloop()

    def save_and_close(self, root, i):
        # Captura a tela do root
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        ImageGrab.grab(bbox=(x, y, x + width, y + height)).save(f"image{i}.png")
        # Fecha o root
        root.destroy()

    def get_n_mortos (self, x, y):
        return self.informations[(x, y)][0]

    def get_n_civis_abrigo (self, x, y):
        return self.informations[(x, y)][2]

    def get_n_feridos (self, x, y):
        return self.informations[(x, y)][1]

    def affected_point (self, position):
        if position in self.affected_points:
            return True
        return False

    def draw_points(self):
        for key, value in self.points.items():
            x_cell, y_cell = key
            color = value
            self.canvas.create_oval(x_cell * self.CELL_SIZE - 5, y_cell * self.CELL_SIZE - 5, x_cell * self.CELL_SIZE + 5, y_cell * self.CELL_SIZE + 5, fill=color, outline=color)
        self.canvas.pack()

    def draw_road(self):
        for line in self.road_points:
            x1, y1, x2, y2 = line
            self.canvas.create_line(x1 * self.CELL_SIZE, y1 * self.CELL_SIZE, x2 * self.CELL_SIZE, y2 * self.CELL_SIZE, fill='black', width=5)

    def get_color(self, population):
        if population < 25:
            return "#d3d3d3"
        elif population < 125:
            return "#a9a9a9"
        else:
            return "#696969"

    # Terramoto
    def calculate_color_earthquake (self, gravity, distance):
        max_intensity = 100
        min_intensity = 255
        intensity = max_intensity - int((distance / gravity) * (max_intensity - min_intensity))
        color = f'#{intensity:02x}0000'
        if color not in self.legend_colors_earthquake:
            self.legend_intensity_earthquake.append(intensity)
            self.legend_colors_earthquake.append(color)
        return color

    def terramoto (self):
        epicenter_x = random.randint(3, 18)
        epicenter_y = random.randint(3, 18)
        gravity = 2
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                if self.population_data[i][j] == 0:
                    self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE, i * self.CELL_SIZE + self.CELL_SIZE, j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill='light blue')
                else:
                    if distance <= gravity:
                        color = self.calculate_color_earthquake(gravity, distance)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            (i + 1) * self.CELL_SIZE, (j + 1) * self.CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos_c = int(self.population_data [i][j] * random.randint (1, 10) * 0.01)
                        n_feridos_c = int(self.population_data[i][j] * random.randint(20, 50) * 0.01)
                        n_civis_abrigo_c = int(self.population_data[i][j] * random.randint(10, 30) * 0.01)
                        self.n_mortos += n_mortos_c
                        self.n_feridos += n_feridos_c
                        self.n_civis_abrigo += n_civis_abrigo_c
                        self.informations [(i, j)][0] = n_mortos_c
                        self.informations[(i, j)][1] = n_feridos_c
                        self.informations[(i, j)][2] = n_civis_abrigo_c
                        if any((i, j) in self.points for i, j in self.points.keys()):
                            self.affected_services.append([i, j])
                        self.affected_points.append([i, j])
                    else:
                        population = self.population_data[i][j]
                        color = self.get_color(population)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                                i * self.CELL_SIZE + self.CELL_SIZE,
                                                j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill=color)
        tk.Label(self.legend_frame, text="Grau de destruição Terramoto:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(self.legend_colors_earthquake)):
            intensity = self.legend_intensity_earthquake [i]
            color = self.legend_colors_earthquake [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(self.legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)

    # Tsunami
    def calculate_color_tsunami(self, distance_sea, distance_tsunami):
        max_intensity = 255
        min_intensity = 100
        intensity = min_intensity + int((distance_sea / distance_tsunami) * (max_intensity - min_intensity))
        intensity = max(min_intensity, min(max_intensity, intensity))
        color = f'#0000{intensity:02x}'
        if color not in self.legend_colors_tsunami:
            self.legend_intensity_tsunami.append(intensity)
            self.legend_colors_tsunami.append(color)
        return color

    def calculate_distance_sea (self, i, j):
        min_distance = 50
        for point in self.sea_points:
            distance = max(abs(point[0] - i), abs(point[1] - j))
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def tsunami (self):
        distance_tsunami = 2
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                distance_sea = self.calculate_distance_sea (i, j)
                if self.population_data[i][j] == 0:
                    self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            i * self.CELL_SIZE + self.CELL_SIZE,
                                            j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill='light blue')
                else:
                    if distance_sea <= distance_tsunami and distance_sea != 0:

                        color = self.calculate_color_tsunami(distance_sea, distance_tsunami)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            (i + 1) * self.CELL_SIZE, (j + 1) * self.CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos_c = int(self.population_data[i][j] * random.randint(1, 10) * 0.01)
                        n_feridos_c = int(self.population_data[i][j] * random.randint(20, 50) * 0.01)
                        n_civis_abrigo_c = int(self.population_data[i][j] * random.randint(10, 30) * 0.01)
                        self.n_mortos += n_mortos_c
                        self.n_feridos += n_feridos_c
                        self.n_civis_abrigo += n_civis_abrigo_c
                        self.informations[(i, j)][0] = n_mortos_c
                        self.informations[(i, j)][1] = n_feridos_c
                        self.informations[(i, j)][2] = n_civis_abrigo_c
                        if any((i, j) in self.points for i, j in self.points.keys()):
                            self.affected_services.append([i, j])
                        self.affected_points.append([i, j])

                    else:
                        population = self.population_data[i][j]
                        color = self.get_color(population)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                                i * self.CELL_SIZE + self.CELL_SIZE,
                                                j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill=color)
        tk.Label(self.legend_frame, text="Grau de destruição Tsunami:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(self.legend_colors_tsunami)):
            intensity = self.legend_intensity_tsunami [i]
            color = self.legend_colors_tsunami [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(self.legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)

    # Terramoto + Tsunami
    def terramoto_tsunami (self):
        epicenter_x = random.randint(3, 18)
        epicenter_y = random.randint(3, 18)
        gravity = 2
        distance_tsunami = 2
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                distance_sea = self.calculate_distance_sea(i, j)
                if self.population_data[i][j] == 0:
                    self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            i * self.CELL_SIZE + self.CELL_SIZE,
                                            j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill='light blue')
                else:
                    if distance <= gravity and distance_sea <= distance_tsunami and distance_sea != 0:
                        color = 'purple'
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            (i + 1) * self.CELL_SIZE, (j + 1) * self.CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos_c = int(self.population_data[i][j] * random.randint(10, 20) * 0.01)
                        n_feridos_c = int(self.population_data[i][j] * random.randint(35, 50) * 0.01)
                        n_civis_abrigo_c = int(self.population_data[i][j] * random.randint(10, 30) * 0.01)
                        self.n_mortos += n_mortos_c
                        self.n_feridos += n_feridos_c
                        self.n_civis_abrigo += n_civis_abrigo_c
                        self.informations[(i, j)][0] = n_mortos_c
                        self.informations[(i, j)][1] = n_feridos_c
                        self.informations[(i, j)][2] = n_civis_abrigo_c
                        if any((i, j) in self.points for i, j in self.points.keys()):
                            self.affected_services.append([i, j])
                        self.affected_points.append([i, j])
                    elif distance <= gravity and distance_sea != 0:
                        color = self.calculate_color_earthquake(gravity, distance)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            (i + 1) * self.CELL_SIZE, (j + 1) * self.CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos_c = int(self.population_data[i][j] * random.randint(1, 10) * 0.01)
                        n_feridos_c = int(self.population_data[i][j] * random.randint(20, 50) * 0.01)
                        n_civis_abrigo_c = int(self.population_data[i][j] * random.randint(10, 30) * 0.01)
                        self.n_mortos += n_mortos_c
                        self.n_feridos += n_feridos_c
                        self.n_civis_abrigo += n_civis_abrigo_c
                        self.informations[(i, j)][0] = n_mortos_c
                        self.informations[(i, j)][1] = n_feridos_c
                        self.informations[(i, j)][2] = n_civis_abrigo_c
                        if any((i, j) in self.points for i, j in self.points.keys()):
                            self.affected_services.append([i, j])
                        self.affected_points.append([i, j])
                    elif distance_sea <= distance_tsunami and distance_sea != 0:
                        color = self.calculate_color_tsunami(distance_sea, distance_tsunami)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                            (i + 1) * self.CELL_SIZE, (j + 1) * self.CELL_SIZE,
                                            fill=color, outline='')
                        n_mortos_c = int(self.population_data[i][j] * random.randint(1, 10) * 0.01)
                        n_feridos_c = int(self.population_data[i][j] * random.randint(20, 50) * 0.01)
                        n_civis_abrigo_c = int(self.population_data[i][j] * random.randint(10, 30) * 0.01)
                        self.n_mortos += n_mortos_c
                        self.n_feridos += n_feridos_c
                        self.n_civis_abrigo += n_civis_abrigo_c
                        self.informations[(i, j)][0] = n_mortos_c
                        self.informations[(i, j)][1] = n_feridos_c
                        self.informations[(i, j)][2] = n_civis_abrigo_c
                        if any((i, j) in self.points for i, j in self.points.keys()):
                            self.affected_services.append([i,j])
                        self.affected_points.append([i, j])
                    else:
                        population = self.population_data[i][j]
                        color = self.get_color(population)
                        self.canvas.create_rectangle(i * self.CELL_SIZE, j * self.CELL_SIZE,
                                                i * self.CELL_SIZE + self.CELL_SIZE,
                                                j * self.CELL_SIZE + self.CELL_SIZE, outline="black", fill=color)
        tk.Label(self.legend_frame, text="Grau de destruição Terramoto:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(self.legend_colors_earthquake)):
            intensity = self.legend_intensity_earthquake [i]
            color = self.legend_colors_earthquake [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(self.legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="Grau de destruição Tsunami:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(self.legend_colors_tsunami)):
            intensity = self.legend_intensity_tsunami [i]
            color = self.legend_colors_tsunami [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(self.legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)


    #Legendas do Mapa

    def legendas (self):
        self.legend_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.N)
        tk.Label(self.legend_frame, text="População/Mar:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="Menos de 25", bg="#d3d3d3", width=20).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="25 a 125", bg="#a9a9a9", width=20).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="125 ou mais", bg="#696969", fg="white", width=20).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="Mar", bg="light blue", fg="black", width=20).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="Estradas:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        tk.Label(self.legend_frame, text="Estrada", bg="black", fg="white", width=20).pack(anchor=tk.W)
        colors = ('red', 'magenta', 'black')
        color_legend = ("Responder Agents", "Shelter Agents", "Supply Vehicles Agents")
        tk.Label(self.legend_frame, text="Serviços:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range(3):
            color = colors[i]
            subtitle = color_legend[i]
            item_frame = tk.Frame(self.legend_frame, bg="#696969")
            item_frame.pack(side=tk.TOP, anchor="w")
            label = tk.Label(item_frame, text=subtitle, bg="#696969", fg="white")
            label.pack(side=tk.RIGHT)
            canvas = tk.Canvas(item_frame, width=20, height=20, bg="#696969", highlightthickness=0)
            canvas.create_oval(5, 5, 15, 15, fill=color)
            canvas.pack(side=tk.RIGHT)

    def legendas2 (self):
        n_responder_agents = 0
        n_shelter_agents = 0
        n_supply_agents = 0
        self.dados [0] = self.n_mortos
        self.dados [1] = self.n_feridos
        for point in self.affected_services:
            i, j = point[0], point[1]
            if (i, j) in self.points:
                color = self.points[(i, j)]
                if color == 'red':
                    n_responder_agents += 1
                elif color == 'magenta':
                    n_shelter_agents += 1
                else:
                    n_supply_agents += 1
        self.dados [2] = n_responder_agents
        self.dados [3] = n_shelter_agents
        self.dados [4] = n_supply_agents
        self.dados [5] = self.n_civis_abrigo
        for i in range(len(self.descricoes)):
            descricao = self.descricoes[i]
            valor = self.dados[i]
            label_descricao = tk.Label(self.root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            label_valor = tk.Label(self.root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")




