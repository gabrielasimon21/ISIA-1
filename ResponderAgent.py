import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import ast
import random


class ResponderAgent(Agent):
    def __init__(self, jid, password, number, current_location, environment):
        super().__init__(jid, password)
        self.number = number
        self.current_location = current_location
        self.environment = environment

    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        self.add_behaviour(ResponderRun(self, self.current_location, self.environment), template)

class ResponderRun(CyclicBehaviour):
    def __init__(self, agent, location, map):
        super().__init__()
        self.agent = agent
        self.location = location
        self.position = [0, 0]
        self.information = [0, 0]
        self.lock = asyncio.Lock()
        self.map = map

    async def respond_proposals(self, civil, propose_messages, position, informations):
        max = 0
        best_agent = None
        refusal_agents = []
        exception = False
        for msg in propose_messages:
            sender = msg.sender
            refusal_agents.append(sender)
            if msg.get_metadata("performative") == "reject":
                continue
            else:
                value = int(msg.get_metadata("value"))
                if value > max:
                    max = value
                    best_agent = sender
        if best_agent == None:
            await self.desconfirm_civil(civil, position)
        else:
            best_agent=str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("value", position)
            msg.set_metadata("value2", informations)
            msg.body = f"ALOCAÇÃO: O agente escolhido para a célula {position} foi o Responder Agent: {best_agent} e encontra-se à distância {max}km"
            try:
                await self.send(msg)
                await self.confirm_civil(civil, best_agent, max)
            except Exception:
                await self.desconfirm_civil(civil, position)
            for agent in refusal_agents:
                if agent != best_agent:
                    agent = str(agent)
                    msg = Message(to=agent)
                    msg.set_metadata("performative", "disconfirm")
                    msg.set_metadata("ontology", "myOntology")
                    msg.set_metadata("language", "OWL-S")
                    msg.body = f"O agente não foi escolhido"
                    try:
                        await self.send(msg)
                    except Exception:
                        pass


    async def confirm_civil(self, civil, agent, dist):
        msg = Message(to=civil)
        msg.set_metadata("performative", "confirm")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"ALOCAÇÃO: Foi alocado o agente {agent} à sua célula"
        try:
            await self.send(msg)
        except Exception:
            pass

    async def desconfirm_civil(self, civil, position):
        msg = Message(to=civil)
        msg.set_metadata("performative", "desconfirm")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"NEGAÇÂO: Não existem agentes disponíveis no momento para a célula {position}"
        try:
            await self.send(msg)
        except Exception:
            pass


    async def send_reject_message(self, agent):
        msg = Message(to=agent)
        msg.set_metadata("performative", "reject")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"Request rejected: Agent busy"
        try:
            await self.send(msg)
        except Exception:
            pass

    def get_distance(self, position):
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    async def send_proposal_message(self, agent, position):
        proposal_value = self.get_distance(position)
        msg = Message(to=agent)
        msg.set_metadata("performative", "propose")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.set_metadata("value", str(proposal_value))
        msg.body = f"Proposta com valor: {proposal_value}"
        try:
            await self.send(msg)
        except Exception:
            pass

    def get_rescue_time(self, information):
        time = information[0] * 0.1 + information [1] * 0.1 #Resgate de 10 feridos e 10 mortos p/h
        return time


    async def run(self):
        async with self.lock:
            msg = await self.receive(timeout=1)
            if msg:
                sender = str(msg.sender)
                position = msg.get_metadata("value")
                if msg.get_metadata("performative") == "inform":
                    print(msg.body)
                    information = msg.get_metadata("value2")
                    self.position = ast.literal_eval(position)
                    self.information = ast.literal_eval(information)
                    #CONTRACT NET
                    for i in range(20):
                        if i != self.agent.number:
                            agent = f"responder{i}@localhost"
                            msg = Message(to=agent)
                            msg.set_metadata("performative", "request")
                            msg.set_metadata("ontology", "myOntology")
                            msg.set_metadata("language", "OWL-S")
                            msg.set_metadata("value", position)
                            msg.body = f"Está disponível? Quanto tempo demora?"
                            try:
                                await self.send(msg)
                            except Exception:
                                pass
                    propose_messages = []
                    for i in range(19):
                        msg = await self.receive(timeout=1)
                        if msg and msg.get_metadata("performative") == "propose":
                            propose_messages.append(msg)
                    await self.respond_proposals(sender, propose_messages, position, information)
                elif msg.get_metadata("performative") == "request":
                    position = ast.literal_eval(position)
                    await self.send_proposal_message(sender, position)
                elif msg.get_metadata("performative") == "confirm":
                    print(msg.body)
                    information = msg.get_metadata("value2")
                    self.position = ast.literal_eval(position)
                    self.information = ast.literal_eval(information)
                    time = self.get_distance(self.position) * 0.05  # 20 km/h
                    delay = random.randint(0, 3) * 0.05 #Estrada cortada
                    await asyncio.sleep(time + delay)
                    self.agent.current_location = self.position
                    time = self.get_rescue_time(self.information)
                    await asyncio.sleep(time)
                    self.map.dados[6] += self.information[0]
                    self.map.dados[7] += self.information[1]






