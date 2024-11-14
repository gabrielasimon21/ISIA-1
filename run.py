import asyncio
from ResponderAgent import ResponderAgent
from SupplyVehicleAgent import SupplyVehicleAgent
from civil_agent import Civil
from ShelterAgent import ShelterAgent
from map import Map
import sys
import tkinter as tk


def update_gui(i, map, dados, rec_nao_uti):
    root = tk.Tk()
    frame = tk.Frame(root)
    root.title(f"Dados de salvamento após {i} horas: ")
    frame.grid(column=0, row=0, padx=10, pady=10)
    legendas(map, root, dados, rec_nao_uti)
    root.mainloop()

def legendas (map, root, dados_atua, rec_uti):
    dados = ["String"] * 10
    descricoes = ["Nº de mortos: ", "Nº de feridos: ", "Nº de civis a necessitar de abrigo: ", "Nº de mortos resgatados: ", "Nº de feridos resgatados: ", "Nº de civis abrigados: ", "Comida utilizada: ", "Água utilizada: ", "Medicamentos utilizados: ", "Nº de recusas: "]
    dados [0] = f"{map.dados[0]}"
    dados [1] = f"{map.dados[1]}"
    dados [2] = f"{map.dados[2]}"
    dados [3] = f"{dados_atua[0]} ({((dados_atua[0]/map.dados[0])*100):.2f}%)"
    dados [4] = f"{dados_atua[1]} ({((dados_atua[1]/map.dados[1])*100):.2f}%)"
    dados [5] = f"{dados_atua[2]} ({((dados_atua[2]/map.dados[2])*100):.2f}%)"
    dados [6] = f"{rec_uti['food']:.2f} ({((map.rec_ent['food']/rec_uti['food'])*100):.2f}%)"
    dados [7] = f"{rec_uti['water']:.2f} ({((map.rec_ent['water']/rec_uti['water'])* 100):.2f}%)"
    dados [8] = f"{rec_uti['medical_supplies']:.2f} ({((map.rec_ent['medical_supplies']/rec_uti['medical_supplies'])* 100):.2f}%)"
    dados [9] = f"{map.n_recusas} ({((map.n_recusas / map.n_pedidos) * 100):.2f}%)"
    for i in range(len(descricoes)):
        descricao = descricoes[i]
        valor = dados[i]
        label_descricao = tk.Label(root, text=descricao)
        label_descricao.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        label_valor = tk.Label(root, text=valor)
        label_valor.grid(row=i, column=1, padx=10, pady=5, sticky="w")

async def stop_running(map, n_shelter):
    dados = []
    dados.append(map.dados[6])
    dados.append(map.dados[7])
    dados.append(map.dados[8])
    rec_ut = {"food": n_shelter*100, "water": n_shelter*100, "medical_supplies": n_shelter*50}
    resources = ["food", "water", "medical_supplies"]
    for agent in shelter_agents.values():
        i = 0
        for value in agent.supply_status.values():
            rec_ut[resources[i]] -= value
            i += 1
    i = 0
    for value in map.rec_ent.values():
        rec_ut[resources[i]] += value
        i += 1
    update_gui(36, map, dados, rec_ut)
    for agent in civil_agents.values():
        await agent.stop()
    for agent in responder_agents.values():
        await agent.stop()
    for agent in shelter_agents.values():
        await agent.stop()
    for agent in supply_agents.values():
        await agent.stop()
    sys.exit(0)


civil_agents = {}
responder_agents = {}
supply_agents = {}
shelter_agents = {}
n_shelter = 0
map = Map()

async def main():
    global n_shelter, map
    map.create_gui()
    affected_points = map.affected_points

    supply_points = map.get_supply_points()
    i = 1
    for point in supply_points: #5, 5
        for j in range(5):
            supply_agents[i] = SupplyVehicleAgent(f"supply{i}@localhost", "password", point, ["food", "water", "medical_supplies"], 800, map)
            i += 1

    supply_inic = []
    for j in range (1, 10):
        if supply_agents[j].current_location not in affected_points:
            await supply_agents[j].start(auto_register=True)
            supply_inic.append(j)

    shelter_points = map.get_shelter_points()
    i = 1
    for point in shelter_points: #4, 4, 4
        for j in range (4):
            shelter_agents[i] = ShelterAgent(f"shelter{i}@localhost", "password", i, point, 200, map, supply_inic)
            i += 1

    shelter_inic_c = []
    shelter_inic = []
    for j in range (1, 7):
        if shelter_agents[j].location not in affected_points:
            await shelter_agents[j].start(auto_register=True)
            shelter_inic.append(j)
    for j in range(7, 13):
        if shelter_agents[j].location not in affected_points:
            await shelter_agents[j].start(auto_register=True)
            shelter_inic_c.append(j)

    n_shelter += len(shelter_inic) + len(shelter_inic_c)

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

    responder_inic_c = []
    responder_inic = []

    for j in range (11, 21):
        if responder_agents[j].current_location not in affected_points:
            await responder_agents[j].start(auto_register=True)
            responder_inic.append(j)
    for j in range(1, 11):
        if responder_agents[j].current_location not in affected_points:
            await responder_agents[j].start(auto_register=True)
            responder_inic_c.append(j)

    k = 0
    for i in range(20):
        for j in range(20):
            if [i, j] in affected_points:
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], True, False, responder_inic_c, shelter_inic_c)
                k += 1
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, True, responder_inic_c, shelter_inic_c)
                k += 1

    for civil_agent in civil_agents.values():
        await civil_agent.start(auto_register=True)

async def run_with_timeout():
    try:
        await asyncio.wait_for(main(), timeout=75)
    except asyncio.TimeoutError:
        await stop_running(map, n_shelter)

if __name__ == "__main__":
    asyncio.run(run_with_timeout())


