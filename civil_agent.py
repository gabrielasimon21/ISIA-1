import spade
import tkinter as tk
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
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
        if self.leader:
            print("Agente iniciado")
            print("SenderAgent started")
            b = self.InformBehav()
            self.add_behaviour(b)
            self.n_mortos = self.environment.get_n_mortos(self.position[0], self.position[1])  # Corrija para chamar o método corretamente
            self.n_feridos = self.environment.get_n_feridos(self.position[0], self.position[1])  # Corrija para chamar o método corretamente

    def communicate(self):
        if self.leader:
            print(f"Nº de mortos: {self.n_mortos}, Nº de feridos: {self.n_feridos}")

    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="shelter1@localhost")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
            msg.set_metadata("language", "OWL-S")  # Set the language of the message content
            msg.body = "Hello World"  # Set the message content
            await self.send(msg)
            print("Message sent!")
            self.exit_code = "Job Finished!"  # Set exit_code for the behaviour
            await self.agent.stop()  # Stop agent from behaviour



