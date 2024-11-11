import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import ast
import random

class ShelterAgent(Agent):
    def __init__(self, jid, password, number, location, capacity, environment):
        super().__init__(jid, password)
        self.number = number
        self.location = location  
        self.capacity = capacity  
        self.current_occupancy = 0  
        self.supply_status = {"food": 100, "water": 100, "medical_supplies": 50}  
        self.resource_requirements = {"food": 0, "water": 0, "medical_supplies": 0} 
        self.urgency_level = 0  
        self.emergency_status = False 
        self.environment = environment

    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        self.add_behaviour(ShelterRun(self, self.location, self.environment), template)

class ShelterRun(CyclicBehaviour):
    def __init__(self, agent, location, map):
        super().__init__()
        self.agent = agent
        self.location = location
        self.position = [0, 0]
        self.information = [0, 0]
        self.lock = asyncio.Lock()
        self.map = map

    async def confirm_civil(self, civil, agent):
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
        msg.body = f"NEGAÇÃO SHELTER: Não existem Shelter agents disponíveis no momento para a célula {position}"
        try:
            await self.send(msg)
        except Exception:
            pass

    async def respond_proposals(self, civil, propose_messages, position, informations):
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
            await self.desconfirm_civil(civil, position)
        else:
            best_agent = str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("value", position)
            msg.set_metadata("value2", informations)
            msg.body = f"ALOCAÇÃO SHELTER: O agente escolhido para a célula {position} foi o Shelter Agent: {best_agent} e encontra-se à distância {max}km"
            try:
                await self.send(msg)
                await self.confirm_civil(civil, best_agent)
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


    def check_availability(self, civilians):
        return self.agent.current_occupancy + civilians <= self.agent.capacity

    async def send_proposal_message(self, position, information, agent):
        if self.check_availability(information):
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

    async def check_resources(self):
        for resource, amount in self.agent.supply_status.items():
            if amount < (0.2 * self.agent.capacity):
                print(f"RESOURCE - {self.agent.jid}: {resource} está abaixo de 20%, pedido de mais")
                await self.request_resources()
                break

    def update_resource_requirements(self):
        self.agent.resource_requirements["food"] = self.agent.current_occupancy * 2
        self.agent.resource_requirements["water"] = self.agent.current_occupancy * 3
        self.agent.resource_requirements["medical_supplies"] = self.agent.current_occupancy * 0.1
        self.update_urgency()

    async def request_resources(self):
        self.update_resource_requirements()
        for i in range(1, 10):
            agent = f"supply{i}@localhost"
            msg = Message(to=agent)
            location = str(self.location)
            resource_requirements = str(self.agent.resource_requirements)
            urgency = str(self.agent.urgency_level)
            msg.set_metadata("performative", "request")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("position", location)
            msg.set_metadata("urgency", urgency)
            msg.set_metadata("resources", resource_requirements)
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
        await self.respond_proposals_supply(propose_messages)

    async def respond_proposals_supply(self, propose_messages):
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
            print(f"NEGAÇÃO SUPPLY: O Shelter agent {self.agent.jid} não conseguiu obter mais recursos")
        else:
            best_agent = str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("value", self.location)
            msg.set_metadata("position", self.agent.location)
            msg.set_metadata("urgency", self.agent.urgency_level)
            msg.set_metadata("resources", self.agent.resource_requirements)
            msg.body = f"REABASTECIMENTO: O agente escolhido para a célula {self.position} foi o Supply Agent: {best_agent} e encontra-se à distância {max}km"
            try:
                await self.send(msg)
                await self.receive_resources(self.agent.resource_requirements)
            except Exception:
                print(f"NEGAÇÃO SUPPLY: O Shelter agent {self.agent.jid} não conseguiu obter mais recursos")
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

    def update_urgency(self):
        food_shortage = self.agent.resource_requirements["food"] - self.agent.supply_status["food"]
        water_shortage = self.agent.resource_requirements["water"] - self.agent.supply_status["water"]
        medical_shortage = self.agent.resource_requirements["medical_supplies"] - self.agent.supply_status["medical_supplies"]

        max_shortage = max(food_shortage, water_shortage, medical_shortage)
        if max_shortage > 0:
            if max_shortage > self.agent.capacity * 0.5:
                self.urgency_level = 5  # High urgency
            elif max_shortage > self.agent.capacity * 0.2:
                self.urgency_level = 3  # Medium urgency
            else:
                self.urgency_level = 1  # Low urgency
        else:
            self.urgency_level = 0

    async def receive_resources(self, instruction):
        delivered_resources = instruction["delivered_resources"]
        for resource, quantity in delivered_resources.items():
            self.agent.supply_status[resource] += quantity
        print(f"Received resources: {delivered_resources}")

    def get_rescue_time(self, information):
        time = information * 0.05 #Resgate de 20 civis p/h
        return time

    def get_distance(self, position):
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    def spend_resources(self):
        self.agent.supply_status['food'] -= self.agent.current_occupancy * 0.1
        self.agent.supply_status['water'] -= self.agent.current_occupancy * 0.1
        self.agent.supply_status['medical_supplies'] -= self.agent.current_occupancy * 0.01
        for resource in self.agent.supply_status:
            if self.agent.supply_status[resource] < 0:
                self.agent.supply_status[resource] = 0

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
                    self.information = int(information)
                    #CONTRACT NET
                    for i in range(20):
                        if i != self.agent.number:
                            agent = f"shelter{i}@localhost"
                            msg = Message(to=agent)
                            msg.set_metadata("performative", "request")
                            msg.set_metadata("ontology", "myOntology")
                            msg.set_metadata("language", "OWL-S")
                            msg.set_metadata("value", position)
                            msg.set_metadata("value2", information)
                            msg.body = f"Está disponível? Quanto tempo demora?"
                            try:
                                await self.send(msg)
                            except Exception:
                                pass
                    shelter_propose_messages = []
                    for i in range(19):
                        msg = await self.receive(timeout=1)
                        if msg and msg.get_metadata("performative") == "propose":
                            shelter_propose_messages.append(msg)
                    await self.respond_proposals(sender, shelter_propose_messages, position, information)
                elif msg.get_metadata("performative") == "request":
                    information = msg.get_metadata("value2")
                    information = int(information)
                    self.position = ast.literal_eval(position)
                    self.information = information
                    await self.send_proposal_message(self.position, self.information, sender)
                elif msg.get_metadata("performative") == "confirm":
                    print(msg.body)
                    information = msg.get_metadata("value2")
                    information = int(information)
                    self.position = ast.literal_eval(position)
                    self.information = information
                    time = self.get_distance(self.position) * 0.05  # 20 km/h
                    delay = random.randint(0, 3) * 0.05  # Estrada cortada
                    await asyncio.sleep(time + delay)
                    self.agent.current_location = self.position
                    time = self.get_rescue_time(self.information)
                    await asyncio.sleep(time)
                    self.agent.current_occupancy += information
                    self.map.dados[8] += self.information
        self.spend_resources()
        await self.check_resources()

