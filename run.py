import asyncio
from ResponderAgent import ResponderAgent
from civil_agent import Civil
from map import Map
import sys
import tkinter as tk


def update_gui(i, map):
    root = tk.Tk()
    frame = tk.Frame(root)
    root.title(f"Dados de salvamento após {i} horas: ")
    frame.grid(column=0, row=0, padx=10, pady=10)
    legendas(map, root)
    root.mainloop()

def legendas (map, root):
    dados = [0]*6
    descricoes = ["Nº de mortos: ", "Nº de feridos: ", "Nº de civis a necessitar de abrigo: ", "Nº de mortos resgatados: ", "Nº de feridos resgatados: ", "Nº de civis abrigados: "]
    dados [0] = map.dados[0]
    dados [1] = map.dados[1]
    dados [2] = map.dados[2]
    dados [3] = map.dados[6]
    dados [4] = map.dados[7]
    dados [5] = map.dados[8]
    for i in range(len(descricoes)):
        descricao = descricoes[i]
        valor = dados[i]
        label_descricao = tk.Label(root, text=descricao)
        label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        label_valor = tk.Label(root, text=valor)
        label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")


async def stop_agents(civil_agents, responder_agents, map):
    for agent in civil_agents.values():
        await agent.stop()
    for agent in responder_agents.values():
        await agent.stop()
    update_gui(48, map)
    sys.exit(0)

civil_agents = {}
responder_agents = {}

async def main():
    map = Map()
    map.create_gui()
    affected_points = map.affected_points
    k = 0

    responder_points = map.get_responder_points()
    i = 1
    for point in responder_points: #3, 3, 3, 3, 4, 4
        if i < 13:
            for j in range (3):
                if i <= 10:
                    responder_agents[i]= ResponderAgent(f"responder{i}@localhost", "password", i, point, map)
                else:
                    responder_agents[i] = ResponderAgent(f"responder{i}@localhost", "password", i, point, map)
                i += 1
        else:
            for j in range (4):
                responder_agents[i] = ResponderAgent(f"responder{i}@localhost", "password", i, point, map)
                i += 1
    #shelter_agent = ShelterAgent("shelter1@localhost", "password", [0, 0], 10, map)
    #await shelter_agent.start(auto_register=True)
    responder_inic_c = []
    responder_inic = []
    for j in range (11, 21):
        if responder_agents[j].current_location not in affected_points:
            await responder_agents[j].start(auto_register=True)
            responder_inic_c.append(j)
    for j in range(1, 11):
        if responder_agents[j].current_location not in affected_points:
            await responder_agents[j].start(auto_register=True)
            responder_inic.append(j)

    for i in range(20):
        for j in range(20):
            if [i, j] in affected_points:
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], True, False, False, False, responder_inic_c)
                k += 1

    for civil_agent in civil_agents.values():
        await civil_agent.start(auto_register=True)

    #asyncio.ensure_future(update_map(map, 0))
    await asyncio.sleep(50)
    await stop_agents(civil_agents, responder_agents, map)



if __name__ == "__main__":
    asyncio.run(main())

