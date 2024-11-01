import threading
import asyncio
import tkinter as tk
from civil_agent import Civil
from ShelterAgent import ShelterAgent
from map import Map
from PIL import Image

async def main():
    map = Map()
    map.create_gui()
    mapa = Image.open('image1.png')
    mapa.show()
    leg = Image.open('image2.png')
    leg.show()
    affected_points = map.affected_points
    civil_agents = {}
    k = 0
    for i in range(20):
        for j in range(20):
            if [i, j] in affected_points:
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], True, False, False, False)
                k += 1
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, True, False, False)
                k += 1
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, False, True, False)
                k += 1
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, False, False, True)
                k += 1

    shelter_agent = ShelterAgent("shelter1@localhost", "password", [0, 0], 10, map)
    await shelter_agent.start(auto_register=True)
    for civil_agent in civil_agents.values():
        await civil_agent.start(auto_register=True)


if __name__ == "__main__":
    asyncio.run(main())
