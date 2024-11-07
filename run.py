import threading
import asyncio
import tkinter as tk
from ResponderAgent import ResponderAgent
from civil_agent import Civil
from ShelterAgent import ShelterAgent
from map import Map
from PIL import Image
#from ResponderAgent import ResponderAgent

async def main():
    map = Map()
    map.create_gui()
    affected_points = map.affected_points
    civil_agents = {}
    responder_agents = {}
    k = 0
    for i in range(20):
        for j in range(20):
            if [i, j] in affected_points:
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], True, False, False, False)
                k += 1
                #civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, True, False, False)
                #k += 1
                #civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, False, True, False)
                #k += 1
                #civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, False, False, True)
                #k += 1

    responder_points = map.get_responder_points()
    i = 1
    for point in responder_points: #3, 3, 3, 3, 4, 4
        if i < 13:
            for j in range (3):
                if i <= 10:
                    responder_agents[i]= ResponderAgent(f"responder{i}@localhost", "password", i, point, False, map)
                else:
                    responder_agents[i] = ResponderAgent(f"responder{i}@localhost", "password", i, point, False, map)
                i += 1
        else:
            for j in range (4):
                responder_agents[i] = ResponderAgent(f"responder{i}@localhost", "password", i, point, 4, map)
                i += 1
    #shelter_agent = ShelterAgent("shelter1@localhost", "password", [0, 0], 10, map)
    #await shelter_agent.start(auto_register=True)
    for j in range (11, 21):
        await responder_agents[j].start(auto_register=True)
    for j in range(1, 11):
        await responder_agents[j].start(auto_register=True)
    for civil_agent in civil_agents.values():
        await civil_agent.start(auto_register=True)



if __name__ == "__main__":
    asyncio.run(main())
