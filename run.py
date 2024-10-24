import asyncio
import logging
from civil_agent import Civil
from ShelterAgent import ShelterAgent
from map import Map

logging.basicConfig(level=logging.DEBUG)

async def main():
    try:
        map = Map()
        map.create_gui()

        civil_agents = {}
        k = 1
        for i in range(20):
            for j in range(20):
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], True, False, False)
                n_civis_criados = 1
                k += 1
                for n in range(map.informations[(i, j)][0]):
                    civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, True, False)
                    n_civis_criados += 1
                    k += 1
                for n in range(map.informations[(i, j)][1]):
                    civil_agents[k] = Civil(f"civil{k}@localhost", "password", map, [i, j], False, False, True)
                    n_civis_criados += 1
                    k += 1

        for civil_agent in civil_agents.values():
            await civil_agent.start(auto_register=True)
            if civil_agent.leader:
                print("Sender started")

        shelter_agent = ShelterAgent("shelter1@localhost", "password", [0, 0], 10, map)
        await shelter_agent.start(auto_register=True)
        print("Receiver started")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
