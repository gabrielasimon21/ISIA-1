import spade
import tkinter as tk
import random

class MapAgent(spade.agent.Agent):
    async def setup(self):
        print("Agente Iniciado!")


GRID_SIZE = 20
CELL_SIZE = 30
fenomenos = ("Terramoto", "Terramoto + Tsunami", "Tsunami")
fenomeno = random.choice(fenomenos)


# Função que inicia a interface gráfica
def create_gui(root, root2, fenomeno):

    #População em cada célula
    population_data = [[66, 117, 80, 149, 140, 54, 145, 21, 132, 51, 140, 25, 135, 122, 27, 34, 65, 90, 156, 98], [130, 126, 93, 57, 144, 152, 62, 54, 26, 139, 22, 152, 65, 78, 35, 101, 139, 149, 146, 145], [135, 15, 100, 105, 124, 157, 106, 45, 111, 120, 151, 98, 58, 52, 34, 92, 42, 140, 97, 23], [44, 125, 138, 103, 29, 30, 141, 84, 49, 32, 147, 66, 33, 26, 37, 102, 146, 134, 160, 107], [122, 154, 111, 32, 125, 106, 97, 21, 63, 88, 111, 106, 75, 19, 93, 138, 156, 108, 80, 88], [76, 83, 142, 120, 39, 139, 154, 48, 122, 63, 50, 79, 117, 116, 99, 101, 103, 47, 39, 103], [158, 61, 123, 70, 140, 67, 149, 94, 70, 27, 136, 113, 147, 94, 132, 129, 68, 149, 58, 103], [110, 45, 30, 98, 150, 19, 83, 75, 83, 69, 84, 53, 86, 102, 81, 69, 134, 48, 99, 79], [91, 106, 115, 82, 152, 141, 56, 24, 109, 53, 130, 83, 129, 150, 21, 124, 63, 147, 34, 49], [54, 25, 143, 27, 109, 137, 57, 126, 156, 160, 155, 39, 156, 102, 114, 46, 18, 119, 108, 61], [95, 98, 27, 136, 143, 37, 148, 148, 92, 50, 103, 96, 51, 71, 38, 151, 160, 87, 144, 45], [157, 62, 18, 75, 52, 45, 69, 83, 133, 24, 149, 91, 101, 153, 136, 73, 152, 89, 52, 130], [63, 88, 156, 76, 153, 135, 128, 90, 154, 69, 63, 99, 70, 27, 51, 102, 129, 119, 127, 133], [140, 61, 134, 64, 58, 40, 141, 160, 143, 150, 107, 93, 113, 22, 15, 85, 58, 54, 123, 106], [24, 59, 148, 103, 69, 116, 157, 51, 108, 143, 47, 26, 20, 117, 37, 94, 16, 43, 155, 85], [84, 135, 23, 54, 122, 114, 105, 68, 21, 16, 99, 114, 59, 104, 99, 149, 48, 60, 46, 132], [69, 88, 27, 89, 137, 47, 120, 94, 90, 152, 153, 22, 82, 132, 34, 25, 34, 129, 61, 46], [105, 44, 19, 108, 107, 148, 97, 67, 34, 84, 24, 77, 52, 120, 101, 96, 115, 75, 108, 46], [98, 81, 155, 142, 20, 27, 122, 82, 43, 0, 0, 0, 148, 158, 58, 116, 127, 99, 29, 51], [91, 99, 57, 82, 124, 141, 137, 48, 0, 0, 0, 0, 0, 0, 77, 88, 17, 120, 43, 140]]

    global n_mortos, n_feridos, n_feridos_resgatados, n_mortos_resgatados, label_valor_mortos, label_valor_feridos
    n_mortos = 0
    n_feridos = 0
    n_feridos_resgatados = 0
    n_mortos_resgatados = 0
    affected_points = []
    label_valor_mortos = None
    label_valor_feridos = None
    #Desenho Mapa

    root.title(f"Mapa Cidade: {fenomeno}")
    root2.title("Dados de destruição")

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=10, pady=10)

    canvas = tk.Canvas(frame, width= 900, height=600)
    canvas.grid(row=0, column=0)


    def draw_points(canvas, points):
        for key, value in points.items():
            x_cell, y_cell = key
            color = value
            x = x_cell * CELL_SIZE
            y = y_cell * CELL_SIZE
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    canvas.pack()

    def draw_road(canvas, road_points):
        for line in road_points:
            x1, y1, x2, y2 = line
            if (x1, y1) in affected_points:
                if (x2, y2) in affected_points:
                    cortada = random.choice([True, False])
                    if cortada:
                        canvas.create_line(x1 * CELL_SIZE, y1 * CELL_SIZE, x2 * CELL_SIZE, y2 * CELL_SIZE, fill='yellow',
                                       width=5)
                    else:
                        canvas.create_line(x1 * CELL_SIZE, y1 * CELL_SIZE, x2 * CELL_SIZE, y2 * CELL_SIZE, fill='black',
                                           width=5)
                else:
                    canvas.create_line(x1 * CELL_SIZE, y1 * CELL_SIZE, x2 * CELL_SIZE, y2 * CELL_SIZE, fill='black',
                                       width=5)
            else:
                canvas.create_line(x1 * CELL_SIZE, y1 * CELL_SIZE, x2 * CELL_SIZE, y2 * CELL_SIZE, fill='black', width=5)

    road_points = [(7, 17, 7, 15), (7, 16, 7, 15), (7, 15, 7, 15), (18, 13, 7, 13), (17, 13, 7, 13), (16, 13, 7, 13), (15, 13, 7, 13), (14, 13, 7, 13), (13, 13, 7, 13), (12, 13, 7, 13), (11, 13, 7, 13), (10, 13, 7, 13), (9, 13, 7, 13), (8, 13, 7, 13), (7, 13, 7, 13), (17, 9, 7, 9), (16, 9, 7, 9), (15, 9, 7, 9), (14, 9, 7, 9), (13, 9, 7, 9), (12, 9, 7, 9), (11, 9, 7, 9), (10, 9, 7, 9), (9, 9, 7, 9), (8, 9, 7, 9), (7, 9, 7, 9), (17, 1, 17, 7), (17, 2, 17, 7), (17, 3, 17, 7), (17, 4, 17, 7), (17, 5, 17, 7), (17, 6, 17, 7), (17, 7, 17, 7), (5, 1, 5, 19), (5, 2, 5, 19), (5, 3, 5, 19), (5, 4, 5, 19), (5, 5, 5, 19), (5, 6, 5, 19), (5, 7, 5, 19), (5, 8, 5, 19), (5, 9, 5, 19), (5, 10, 5, 19), (5, 11, 5, 19), (5, 12, 5, 19), (5, 13, 5, 19), (5, 14, 5, 19), (5, 15, 5, 19), (5, 16, 5, 19), (5, 17, 5, 19), (5, 18, 5, 19), (5, 19, 5, 19), (19, 19, 19, 17), (19, 18, 19, 17), (19, 17, 19, 17), (17, 7, 19, 7), (18, 7, 19, 7), (19, 7, 19, 7), (18, 15, 18, 13), (18, 14, 18, 13), (18, 13, 18, 13), (1, 1, 1, 19), (1, 2, 1, 19), (1, 3, 1, 19), (1, 4, 1, 19), (1, 5, 1, 19), (1, 6, 1, 19), (1, 7, 1, 19), (1, 8, 1, 19), (1, 9, 1, 19), (1, 10, 1, 19), (1, 11, 1, 19), (1, 12, 1, 19), (1, 13, 1, 19), (1, 14, 1, 19), (1, 15, 1, 19), (1, 16, 1, 19), (1, 17, 1, 19), (1, 18, 1, 19), (1, 19, 1, 19), (7, 11, 17, 11), (8, 11, 17, 11), (9, 11, 17, 11), (10, 11, 17, 11), (11, 11, 17, 11), (12, 11, 17, 11), (13, 11, 17, 11), (14, 11, 17, 11), (15, 11, 17, 11), (16, 11, 17, 11), (17, 11, 17, 11), (11, 1, 13, 1), (12, 1, 13, 1), (13, 1, 13, 1), (13, 7, 15, 7), (14, 7, 15, 7), (15, 7, 15, 7), (19, 7, 19, 1), (19, 6, 19, 1), (19, 5, 19, 1), (19, 4, 19, 1), (19, 3, 19, 1), (19, 2, 19, 1), (19, 1, 19, 1), (19, 17, 7, 17), (18, 17, 7, 17), (17, 17, 7, 17), (16, 17, 7, 17), (15, 17, 7, 17), (14, 17, 7, 17), (13, 17, 7, 17), (12, 17, 7, 17), (11, 17, 7, 17), (10, 17, 7, 17), (9, 17, 7, 17), (8, 17, 7, 17), (7, 17, 7, 17), (5, 19, 19, 19), (6, 19, 19, 19), (7, 19, 19, 19), (8, 19, 19, 19), (9, 19, 19, 19), (10, 19, 19, 19), (11, 19, 19, 19), (12, 19, 19, 19), (13, 19, 19, 19), (14, 19, 19, 19), (15, 19, 19, 19), (16, 19, 19, 19), (17, 19, 19, 19), (18, 19, 19, 19), (19, 19, 19, 19), (17, 11, 17, 9), (17, 10, 17, 9), (17, 9, 17, 9), (7, 9, 7, 1), (7, 8, 7, 1), (7, 7, 7, 1), (7, 6, 7, 1), (7, 5, 7, 1), (7, 4, 7, 1), (7, 3, 7, 1), (7, 2, 7, 1), (7, 1, 7, 1), (13, 1, 13, 7), (13, 2, 13, 7), (13, 3, 13, 7), (13, 4, 13, 7), (13, 5, 13, 7), (13, 6, 13, 7), (13, 7, 13, 7), (9, 7, 11, 7), (10, 7, 11, 7), (11, 7, 11, 7), (7, 1, 9, 1), (8, 1, 9, 1), (9, 1, 9, 1), (9, 1, 9, 7), (9, 2, 9, 7), (9, 3, 9, 7), (9, 4, 9, 7), (9, 5, 9, 7), (9, 6, 9, 7), (9, 7, 9, 7), (7, 15, 19, 15), (8, 15, 19, 15), (9, 15, 19, 15), (10, 15, 19, 15), (11, 15, 19, 15), (12, 15, 19, 15), (13, 15, 19, 15), (14, 15, 19, 15), (15, 15, 19, 15), (16, 15, 19, 15), (17, 15, 19, 15), (18, 15, 19, 15), (19, 15, 19, 15), (3, 1, 5, 1), (4, 1, 5, 1), (5, 1, 5, 1), (15, 7, 15, 1), (15, 6, 15, 1), (15, 5, 15, 1), (15, 4, 15, 1), (15, 3, 15, 1), (15, 2, 15, 1), (15, 1, 15, 1), (1, 19, 3, 19), (2, 19, 3, 19), (3, 19, 3, 19), (11, 7, 11, 1), (11, 6, 11, 1), (11, 5, 11, 1), (11, 4, 11, 1), (11, 3, 11, 1), (11, 2, 11, 1), (11, 1, 11, 1), (15, 1, 17, 1), (16, 1, 17, 1), (17, 1, 17, 1), (3, 19, 3, 1), (3, 18, 3, 1), (3, 17, 3, 1), (3, 16, 3, 1), (3, 15, 3, 1), (3, 14, 3, 1), (3, 13, 3, 1), (3, 12, 3, 1), (3, 11, 3, 1), (3, 10, 3, 1), (3, 9, 3, 1), (3, 8, 3, 1), (3, 7, 3, 1), (3, 6, 3, 1), (3, 5, 3, 1), (3, 4, 3, 1), (3, 3, 3, 1), (3, 2, 3, 1), (3, 1, 3, 1), (7, 9, 15, 9), (8, 9, 15, 9), (9, 9, 15, 9), (10, 9, 15, 9), (11, 9, 15, 9), (12, 9, 15, 9), (13, 9, 15, 9), (14, 9, 15, 9), (15, 9, 15, 9), (7, 13, 7, 11), (7, 12, 7, 11), (7, 11, 7, 11)]

    points = {(18, 4): 'black', (15, 14): 'black', (18, 20): 'magenta', (10, 8): 'magenta', (2, 8): 'magenta',
              (9, 12): 'red', (17, 6): 'red', (3, 3): 'red', (6, 17): 'red', (4, 6): 'red', (17, 15): 'red'}

    def get_color(population):
        if population == 0:
            return 'light blue'
        elif population < 25:
            return "#d3d3d3"
        elif population < 125:
            return "#a9a9a9"
        else:
            return "#696969"

    legend_colors_earthquake = [0] * 30
    legend_intensity_earthquake = [0] * 30
    legend_colors_tsunami = [0] * 30
    legend_intensity_tsunami = [0] * 30

    #Terramoto

    def calculate_color_earthquake (gravity, distance, legend_colors_earthquake, legend_intensity_earthquake):

        max_intensity = 100
        min_intensity = 255

        intensity = max_intensity - int((distance / gravity) * (max_intensity - min_intensity))

        color = f'#{intensity:02x}0000'

        if color not in legend_colors_earthquake:
            legend_intensity_earthquake.append(intensity)
            legend_colors_earthquake.append(color)

        return color

    if (fenomeno == "Terramoto"):
        epicenter_x = random.randint(3, 18)
        epicenter_y = random.randint(3, 18)
        gravity = random.randint(3, 7)
        affected_services_earthquake = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                if population_data[i][j] == 0:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                else:
                    if distance <= gravity:
                        color = calculate_color_earthquake(gravity, distance, legend_colors_earthquake, legend_intensity_earthquake)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                        point = (i, j)
                        affected_points.append(point)
                    else:
                        x1 = i * CELL_SIZE
                        y1 = j * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE
                        population = population_data[i][j]
                        color = get_color(population)
                        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

    def calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami):
        max_intensity = 255
        min_intensity = 100

        intensity = min_intensity + int((distance_sea / distance_tsunami) * (max_intensity - min_intensity))

        intensity = max(min_intensity, min(max_intensity, intensity))

        color = f'#0000{intensity:02x}'

        if color not in legend_colors_tsunami:
            legend_intensity_tsunami.append(intensity)
            legend_colors_tsunami.append(color)

        return color

    def calculate_distance_sea (i, j):
        sea_points = [( 18 , 9 ) , ( 18 , 10 ) , ( 18 , 11 ) , ( 19 , 8 ) , ( 19 , 9 ) , ( 19 , 10 ) , ( 19 , 11 ) , ( 19 , 12 ) , ( 19 , 13 ) ]

        min_distance = 50
        for point in sea_points:
            distance = max(abs(point[0] - i), abs(point[1] - j))
            if distance < min_distance:
                min_distance = distance
        return min_distance



    if (fenomeno == "Tsunami"):
        distance_tsunami = random.randint(2, 4)
        affected_services_tsunami = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance_sea = calculate_distance_sea (i, j)
                if population_data[i][j] == 0:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                else:
                    if distance_sea <= distance_tsunami and distance_sea != 0:
                        color = calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_tsunami.append(point)
                        point = (i, j)
                        affected_points.append(point)

                    else:
                        x1 = i * CELL_SIZE
                        y1 = j * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE
                        population = population_data[i][j]
                        color = get_color(population)
                        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)


    if (fenomeno == "Terramoto + Tsunami"):
        epicenter_x = random.randint(3, 18)
        epicenter_y = random.randint(3, 18)
        gravity = random.randint(3, 7)
        distance_tsunami = random.randint(2, 4)
        affected_services_earthquake = [[0 for _ in range(50)] for _ in range(50)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                distance = max(abs(epicenter_x - i), abs(epicenter_y - j))
                distance_sea = calculate_distance_sea(i, j)
                if population_data[i][j] == 0:
                    x1 = i * CELL_SIZE
                    y1 = j * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    population = population_data[i][j]
                    color = get_color(population)
                    canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                else:
                    if distance <= gravity and distance_sea <= distance_tsunami and distance_sea != 0:
                        color = 'purple'
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (35, 70) * 0.01
                        n_mortos += population_data[i][j] * random.randint(10, 20) * 0.01
                    elif distance <= gravity and distance_sea != 0:
                        color = calculate_color_earthquake(gravity, distance, legend_colors_earthquake, legend_intensity_earthquake)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                        point = (i, j)
                        affected_points.append(point)
                    elif distance_sea <= distance_tsunami and distance_sea != 0:
                        color = calculate_color_tsunami(distance_sea, distance_tsunami, legend_colors_tsunami, legend_intensity_tsunami)
                        canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                            (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                            fill=color, outline='')
                        n_feridos += population_data [i][j] * random.randint (20, 50) * 0.01
                        n_mortos += population_data[i][j] * random.randint(1, 10) * 0.01
                        if any((i, j) in points for i, j in points.keys()):
                            point = (i, j)
                            affected_services_earthquake.append(point)
                        point = (i, j)
                        affected_points.append(point)
                    else:
                        x1 = i * CELL_SIZE
                        y1 = j * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE
                        population = population_data[i][j]
                        color = get_color(population)
                        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)

    #Legendas do Mapa

    draw_points (canvas, points)
    draw_road(canvas, road_points)
    legend_frame = tk.Frame(root)
    legend_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.N)

    tk.Label(legend_frame, text="População/Mar:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Menos de 25", bg="#d3d3d3", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="25 a 125", bg="#a9a9a9", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="125 ou mais", bg="#696969", fg="white", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Mar", bg="light blue", fg="black", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Estradas:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Estrada", bg="black", fg="white", width=20).pack(anchor=tk.W)
    tk.Label(legend_frame, text="Estrada cortada", bg="yellow", width=20).pack(anchor=tk.W)

    descricoes = ["Nº de mortos: ", "Nº de feridos: ", "Nº Responders (bases) destruídos: ", "Nº de Shelters destruídos: ", "Nº de Supply (bases) destruídas: ", "Nº de mortos resgatados: ", "Nº de feridos resgatados: "]

    if fenomeno == "Terramoto" or fenomeno == "Terramoto + Tsunami":
        tk.Label(legend_frame, text="Grau de destruição Terramoto:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(legend_colors_earthquake)):
            intensity = legend_intensity_earthquake [i]
            color = legend_colors_earthquake [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
        dados = [0] * 7
        n_responder_agents = 0
        n_shelter_agents = 0
        n_supply_agents = 0
        dados [0] = int(n_mortos)
        dados [1] = int(n_feridos)
        for point in affected_services_earthquake:
            i, j = point[0], point[1]
            if (i, j) in points:
                color = points[(i, j)]
                if color == 'red':
                    n_responder_agents += 1
                elif color == 'magenta':
                    n_shelter_agents += 1
                else:
                    n_supply_agents += 1
        dados [2] = n_responder_agents
        dados [3] = n_shelter_agents
        dados [4] = n_supply_agents
        dados [5] = n_mortos_resgatados
        dados [6] = n_feridos_resgatados

        for i in range(len(descricoes)):
            descricao = descricoes[i]
            valor = dados[i]
            label_descricao = tk.Label(root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            label_valor = tk.Label(root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            if descricao == "Nº de mortos resgatados: ":
                label_valor_mortos = label_valor
            elif descricao == "Nº de feridos resgatados: ":
                label_valor_feridos = label_valor

        def update_resgatados():
            global n_mortos_resgatados, n_feridos_resgatados
            if n_mortos_resgatados != n_mortos:
                n_mortos_resgatados += 1
                label_valor_mortos.config(text=n_mortos_resgatados)
            if n_feridos_resgatados != n_feridos:
                n_feridos_resgatados += 1
                label_valor_feridos.config(text=n_feridos_resgatados)
            root2.after(1000, update_resgatados)

        root2.after(1000, update_resgatados)

    if fenomeno == "Tsunami" or fenomeno == "Terramoto + Tsunami":
        tk.Label(legend_frame, text="Grau de destruição Tsunami:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        for i in range (len(legend_colors_tsunami)):
            intensity = legend_intensity_tsunami [i]
            color = legend_colors_tsunami [i]
            if color != 0 and intensity != 0:
                destruction = 1000 / intensity
                tk.Label(legend_frame, text=f"{destruction} ", bg= color, width=20).pack(anchor=tk.W)
    if fenomeno == 'Tsunami':
        dados = [0] * 7
        n_responder_agents = 0
        n_shelter_agents = 0
        n_supply_agents = 0
        dados [0] = int(n_mortos)
        dados [1] = int(n_feridos)
        for point in affected_services_tsunami:
            i, j = point[0], point[1]
            if (i, j) in points:
                color = points[(i, j)]
                if color == 'red':
                    n_responder_agents += 1
                elif color == 'magenta':
                    n_shelter_agents += 1
                else:
                    n_supply_agents += 1
        dados [2] = n_responder_agents
        dados [3] = n_shelter_agents
        dados [4] = n_supply_agents
        dados [5] = n_mortos_resgatados
        dados [6] = n_feridos_resgatados

        for i in range(len(descricoes)):
            descricao = descricoes[i]
            valor = dados[i]
            label_descricao = tk.Label(root2, text=descricao)
            label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            label_valor = tk.Label(root2, text=valor)
            label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            if descricao == "Nº de mortos resgatados: ":
                label_valor_mortos = label_valor
            elif descricao == "Nº de feridos resgatados: ":
                label_valor_feridos = label_valor

        def update_resgatados():
            global n_mortos_resgatados, n_feridos_resgatados
            if n_mortos_resgatados != n_mortos:
                n_mortos_resgatados += 1
                label_valor_mortos.config(text=n_mortos_resgatados)
            if n_feridos_resgatados != n_feridos:
                n_feridos_resgatados += 1
                label_valor_feridos.config(text=n_feridos_resgatados)
            root2.after(1000, update_resgatados)

        root2.after(1000, update_resgatados)


    colors = ('red', 'magenta', 'black')
    color_legend = ("Responder Agents", "Shelter Agents", "Supply Vehicles Agents")
    tk.Label(legend_frame, text="Serviços:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
    for i in range (3):
        color = colors[i]
        subtitle = color_legend[i]
        item_frame = tk.Frame(legend_frame, bg="#696969")
        item_frame.pack(side=tk.TOP, anchor="w")
        label = tk.Label(item_frame, text=subtitle, bg="#696969", fg="white")
        label.pack(side=tk.RIGHT)
        canvas = tk.Canvas(item_frame, width=20, height=20, bg="#696969", highlightthickness=0)
        canvas.create_oval(5, 5, 15, 15, fill=color)
        canvas.pack(side=tk.RIGHT)


if __name__ == "__main__":
    root = tk.Tk()
    root2 = tk.Tk()
    create_gui(root, root2, fenomeno)
    root.mainloop()



