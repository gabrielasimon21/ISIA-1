import spade
import tkinter as tk
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import asyncio

class Civil(Agent):
    def __init__(self, jid, password, environment, position, leader, dead, hurt):
        super().__init__(jid, password)
        self.environment = environment
        self.position = position
        self.leader = leader
        self.dead = dead
        self.hurt = hurt

        async def setup(self):
            class CivilInteraction(CyclicBehaviour):
                async def run(self):
                    print("Agente iniciado")
                    self.affected = environment.affected_points(position)
                    self.n_mortos = environment.n_mortos()
                    self.n_feridos = environment.n_feridos()

                    def communicate (self):
                        if self.affected == True and self.leader == True:
                            print (f"Nº de mortos: {self.n_mortos}, Nº de feridos: {self.n_feridos}")
            self.communicate()
            self.add_behaviour(CivilInteraction())