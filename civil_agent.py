import spade
import tkinter as tk
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import asyncio

class Civil(Agent):
    def __init__(self, jid, password, environment, position, leader, dead, hurt, shelter):
        super().__init__(jid, password)
        self.environment = environment
        self.position = position
        self.leader = leader
        self.dead = dead
        self.hurt = hurt
        self.shleter = shelter
        self.resg1 = False
        self.resg2 = False

    def communicate(self):
        if self.leader:
            print(f"Nº de mortos: {self.n_mortos}, Nº de feridos: {self.n_feridos}")


    async def setup(self):
        self.n_mortos = self.environment.get_n_mortos(self.position[0], self.position[1])
        self.n_feridos = self.environment.get_n_feridos(self.position[0], self.position[1])
        self.n_civis_abrigo = self.environment.get_n_civis_abrigo(self.position[0], self.position[1])
        if self.leader:
            self.add_behaviour(InformBehav(self.n_mortos, self.n_feridos, self.n_civis_abrigo, self.resg1, self.resg2))

class InformBehav(OneShotBehaviour):
    def __init__(self, mortos, feridos, abrigo, resg1, resg2):
        super().__init__()
        self.mortos = mortos
        self.feridos = feridos
        self.abrigo = abrigo
        self.resg1 = resg1
        self.resg2 = resg2

    async def run(self):
        if self.resg1 == False:
            msg = Message(to="responder1@localhost")
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.body = f"Nº de mortos: {self.mortos}, Nº de feridos: {self.feridos}"
            await self.send(msg)
            print("Message sent!")
        if self.resg2 == False:
            msg = Message(to="shelter1@localhost")
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.body = f"Nº de civis necessitam abrigo: {self.abrigo}"
            await self.send(msg)
            print("Message sent!")







