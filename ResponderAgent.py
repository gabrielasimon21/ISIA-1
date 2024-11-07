import asyncio
import spade
from async_timeout import timeout
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.behaviour import OneShotBehaviour
from spade.template import Template
import time
import random
import ast

class ContractNet(CyclicBehaviour):
    def __init__(self, agent, location):
        super().__init__()
        self.agent = agent
        self.location = location

    async def respond_proposals(self, propose_messages, position):
        max = 0
        best_agent = None
        refusal_agents = []
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
            print(f"Não há agentes disponíveis neste momento para a célula {position}")
        else:
            best_agent=str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.body = f"O agente escolhido para a célula {position} foi o Responder Agent: {best_agent} e encontra-se à distância {max}km"
            print(msg.body)
            await self.send(msg)
            for agent in refusal_agents:
                if agent != best_agent:
                    agent = str(agent)
                    msg = Message(to=agent)
                    msg.set_metadata("performative", "disconfirm")
                    msg.set_metadata("ontology", "myOntology")
                    msg.set_metadata("language", "OWL-S")
                    msg.body = f"O agente não foi escolhido"
                    await self.send(msg)


    async def send_reject_message(self, receiver):
        reject_msg = Message(to=receiver)
        reject_msg.set_metadata("performative", "reject")
        reject_msg.set_metadata("ontology", "myOntology")
        reject_msg.set_metadata("language", "OWL-S")
        reject_msg.body = f"Request rejected: Agent busy"
        await self.send(reject_msg)

    def get_distance(self, position):
        position = ast.literal_eval(position)
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    async def send_proposal_message(self, receiver, position):
        proposal_value = self.get_distance(position)
        proposal_msg = Message(to=receiver)
        proposal_msg.set_metadata("performative", "propose")
        proposal_msg.set_metadata("ontology", "myOntology")
        proposal_msg.set_metadata("language", "OWL-S")
        proposal_msg.set_metadata("value", str(proposal_value))
        proposal_msg.body = f"Proposta com valor: {proposal_value}"
        await self.send(proposal_msg)

    async def run(self):
        msg = await self.receive(timeout=5)
        if msg:
            sender = str(msg.sender)
            if msg.get_metadata("performative") == "inform":
                print(f"Received inform message: {msg.body}")
                position = msg.get_metadata("value")
                if not self.agent.busy: #Adicionar tempo de chegada
                    self.agent.busy = True
                    distance = self.get_distance(position)
                    print(f"O agente escolhido para a célula {position} foi o Responder Agent: {self.agent.jid}, e encontra-se à distância {distance}km")
                else:
                    for i in range(20):
                        if i != self.agent.number:
                            msg = Message(to=f"responder{i}@localhost")
                            msg.set_metadata("performative", "request")
                            msg.set_metadata("ontology", "myOntology")
                            msg.set_metadata("language", "OWL-S")
                            msg.set_metadata("value", str(position))
                            msg.body = f"Está disponível? Quanto tempo demora?"
                            await self.send(msg)
                    propose_messages = []
                    for i in range(19):
                        msg = await self.receive(timeout=5)
                        if msg and msg.get_metadata("performative") == "propose":
                            propose_messages.append(msg)
                    await self.respond_proposals(propose_messages, position)
            elif msg.get_metadata("performative") == "request":
                position = msg.get_metadata("value")
                if self.agent.busy:
                    await self.send_reject_message(sender)
                else:
                    await self.send_proposal_message(sender, position)

class ResponderAgent(Agent):
    def __init__(self, jid, password, number, current_location, busy, environment):
        super().__init__(jid, password)
        self.number = number
        self.current_location = current_location
        self.busy = busy
        self.environment = environment

    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        self.add_behaviour(ContractNet(self, self.current_location), template)



