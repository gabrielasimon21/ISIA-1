from symbol import continue_stmt

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random


class Civil(Agent):
    def __init__(self, jid, password, environment, position, leader, leader2, n_responder_agents, n_shelter_agents):
        super().__init__(jid, password)
        self.environment = environment
        self.position = position
        self.leader = leader # Representante dos mortos e feridos
        self.leader2 = leader2 # Representante das essoas deslojadas
        self.resg1 = False # Já resgataram os mortos e feridos
        self.resg2 = False # Já abrigaram os civis desalojados
        self.n_responder_agents = n_responder_agents
        self.n_shelter_agents = n_shelter_agents

    # Função que inicia o comportamento cíclico do agente civil, que é diferente caso seja o representante dos mortos e feridos ou o representante dos civis que necessitam de abrigo
    async def setup(self):
        self.mortos = self.environment.get_n_mortos(self.position[0], self.position[1])
        self.feridos = self.environment.get_n_feridos(self.position[0], self.position[1])
        self.civis_abrigo = self.environment.get_n_civis_abrigo(self.position[0], self.position[1])
        if self.leader:
            try:
                self.add_behaviour(CivilRun(self))
            except Exception as e:
                print(f"ERRO: {e}")
        if self.leader2:
            try:
                self.add_behaviour(CivilRun2(self))
            except Exception as e:
                print(f"ERRO: {e}")

# Classe que representa o comportamento cíclico do civil representante dos mortos e feridos
class CivilRun(CyclicBehaviour):
    def __init__(self, civil):
        super().__init__()
        self.civil = civil
        self.lock = asyncio.Lock()

    # Enquanto os mortos e feridos da célula que este civil representa não forem socorridos, ele envia mensagens de informação a um Responder Agent escolhido aleatoriamente
    async def run(self):
        async with self.lock:
            if self.civil.resg1 == False:
                self.civil.environment.n_pedidos += 1
                i = random.randint(1, self.agent.n_responder_agents)
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
                        self.civil.environment.n_recusas += 1
                        print(msg.body)

# Classe que representa o comportamento cíclico do civil representante dos civis que necessitam de abrigo
class CivilRun2(CyclicBehaviour):
    def __init__(self, civil):
        super().__init__()
        self.civil = civil
        self.lock = asyncio.Lock()

    # Enquanto os civis que necessitam de abrigo da célula que este civil representa não forem socorridos, ele envia mensagens de informação a um Shelter Agent escolhido aleatoriamente
    async def run(self):
        async with self.lock:
            if self.civil.resg2 == False:
                self.civil.environment.n_pedidos += 1
                i = random.randint(1, self.agent.n_shelter_agents)
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
                        self.civil.environment.n_recusas += 1
                        print(msg.body)










