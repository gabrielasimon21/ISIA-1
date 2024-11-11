from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random


class Civil(Agent):
    def __init__(self, jid, password, environment, position, leader, leader2, resp_c, shelt_c):
        super().__init__(jid, password)
        self.environment = environment
        self.position = position
        self.leader = leader
        self.leader2 = leader2
        self.resg1 = False
        self.resg2 = False
        self.resp_c = resp_c
        self.shelt_c = shelt_c

    async def setup(self):
        self.mortos = self.environment.get_n_mortos(self.position[0], self.position[1])
        self.feridos = self.environment.get_n_feridos(self.position[0], self.position[1])
        self.civis_abrigo = self.environment.get_n_civis_abrigo(self.position[0], self.position[1])
        if self.leader:
            self.add_behaviour(CivilRun(self))
        if self.leader2:
            self.add_behaviour(CivilRun2(self))

class CivilRun(CyclicBehaviour):
    def __init__(self, civil):
        super().__init__()
        self.civil = civil
        self.lock = asyncio.Lock()

    async def run(self):
        async with self.lock:
            if self.civil.resg1 == False:
                i = random.choice(self.civil.resp_c)
                agent = f"responder{i}@localhost"
                msg = Message(to=agent)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("ontology", "myOntology")
                msg.set_metadata("language", "OWL-S")
                msg.set_metadata("value", str(self.civil.position))
                value2 = [self.civil.mortos, self.civil.feridos]
                msg.set_metadata("value2", str(value2))
                msg.body = f"INFORMAÇÃO RESPONDER: Nº de mortos: {self.civil.mortos}, Nº de feridos: {self.civil.feridos}, Localização: {self.civil.position}"
                try:
                    await self.send(msg)
                except Exception:
                    pass
                msg = await self.receive(timeout=20)
                if msg:
                    if msg.get_metadata("performative") == "confirm":
                        self.civil.resg1 = True
                    else:
                        print(msg.body)

class CivilRun2(CyclicBehaviour):
    def __init__(self, civil):
        super().__init__()
        self.civil = civil
        self.lock = asyncio.Lock()

    async def run(self):
        async with self.lock:
            if self.civil.resg2 == False:
                i = random.choice(self.civil.shelt_c)
                agent = f"shelter{i}@localhost"
                msg = Message(to=agent)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("ontology", "myOntology")
                msg.set_metadata("language", "OWL-S")
                msg.set_metadata("value", str(self.civil.position))
                value2 = self.civil.civis_abrigo
                msg.set_metadata("value2", str(value2))
                msg.body = f"INFORMAÇÃO SHELTER: Nº de civis a necessitar de abrigo: {self.civil.civis_abrigo}, Localização: {self.civil.position}"
                try:
                    await self.send(msg)
                except Exception:
                    pass
                msg = await self.receive(timeout=20)
                if msg:
                    if msg.get_metadata("performative") == "confirm":
                        self.civil.resg2 = True
                    else:
                        print(msg.body)










