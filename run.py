import spade
import tkinter as tk
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio
from map import Map
from civil_agent import Civil

async def main():
    # Create and initialize the environment
    environment = Map()
    environment.create_gui()
    civil_agents = {}
    k = 1
    for i in range (20):
        for j in range (20):
            population = environment.population_data [i][j]
            civil_agents[k] = Civil(f"civil{k}@localhost", "password", environment,[i, j], True, False, False)
            print (f"Agente{k}")
            n_civis_criados = 1
            k += 1
            for n in range (environment.informations[(i, j)] [0]):
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", environment, [i, j], False, True, False)
                n_civis_criados += 1
                k += 1
                print(f"Agente{k}")
            for n in range (environment.informations[(i, j)] [0]):
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", environment, [i, j], False, False, True)
                n_civis_criados += 1
                k += 1
                print(f"Agente{k}")
            while (n_civis_criados < population):
                civil_agents[k] = Civil(f"civil{k}@localhost", "password", environment, [i, j], False, False, False)
                n_civis_criados += 1
                k += 1
                print(f"Agente{k}")
    for civil_agent in civil_agents.values():
        await civil_agent.start(auto_register=True)

if __name__ == "__main__":
    spade.run(main())