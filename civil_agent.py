from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random


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

    async def setup(self):
        self.n_mortos = self.environment.get_n_mortos(self.position[0], self.position[1])
        self.n_feridos = self.environment.get_n_feridos(self.position[0], self.position[1])
        self.n_civis_abrigo = self.environment.get_n_civis_abrigo(self.position[0], self.position[1])
        if self.leader:
            self.add_behaviour(CivilRun(self, self.n_mortos, self.n_feridos, self.n_civis_abrigo, self.resg1, self.resg2, self.position))

class CivilRun(CyclicBehaviour):
    def __init__(self, agent, mortos, feridos, abrigo, resg1, resg2, position):
        super().__init__()
        self.mortos = mortos
        self.feridos = feridos
        self.abrigo = abrigo
        self.resg1 = resg1
        self.resg2 = resg2
        self.position = position
        self.agent = agent

    async def run(self):
        if self.agent.resg1 == False:
            i = random.randint(1, 10)
            agent = f"responder{i}@localhost"
            msg = Message(to=agent)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("value", str(self.position))
            value2 = [self.mortos, self.feridos]
            msg.set_metadata("value2", str(value2))
            msg.body = f"Nº de mortos: {self.mortos}, Nº de feridos: {self.feridos}, Localização: {self.position}"
            try:
                await self.send(msg)
            except Exception:
                pass
            msg = await self.receive(timeout=10)
            if msg:
                if msg.get_metadata("performative") == "confirm":
                    self.agent.resg1 = True

        #if self.resg2 == False:
            #msg = Message(to="shelter1@localhost")
            #msg.set_metadata("performative", "inform")
            #msg.set_metadata("ontology", "myOntology")
            #msg.set_metadata("language", "OWL-S")
            #msg.body = f"Nº de civis necessitam abrigo: {self.abrigo}"
            #await self.send(msg)
            #print("Message sent!")
        await asyncio.sleep(20)










