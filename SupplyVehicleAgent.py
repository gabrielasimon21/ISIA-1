import ast
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import random
from spade.template import Template

# Classe que representa os Supply Agents
class SupplyVehicleAgent(Agent):
    def __init__(self, jid, password, depot_location, resource_types, vehicle_capacity, environment):
        super().__init__(jid, password)
        self.depot_location = depot_location
        self.resource_types = resource_types  # List of resources (food, water, medical supplies)
        self.current_load = [0, 0, 0]
        self.current_location = depot_location
        self.vehicle_capacity = vehicle_capacity
        self.environment = environment
    # Função que inicia o comportamento cíclico dos Supply Agents
    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        try:
            self.add_behaviour(SupplyVehicleRun(self, self.current_location, self.environment), template)
        except Exception as e:
            print(f"ERRO: {e}")

# Classe que representa o comportamento cíclico dos Supply Agents
class SupplyVehicleRun(CyclicBehaviour):
    def __init__(self, agent, location, map):
        super().__init__()
        self.agent = agent
        self.location = location
        self.position = [0, 0]
        self.lock = asyncio.Lock()
        self.map = map

    # Função que avalia a disponibilidade de um Supply Agent entregar x recursos a um abrigo
    def check_availability(self, required_resources):
        i = 0
        if isinstance(required_resources, dict):
            required_resources = required_resources.items()

        for resource, cap in required_resources:
            if cap > self.agent.current_load[i]:
                return False
            i += 1
        return True

    # Função que calcula a distância a uma determinada célula
    def get_distance(self, position):
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    # Função que envia uma proposta para um Shelter Agent que lhe enviou um request durante o protocolo Contract Net
    async def send_proposal_message(self, position, urgency, resources, agent):
        if self.check_availability(resources):
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

    # Função que entrega os recursos a um abrigo
    async def deliver_resources(self, required_resources, agent):
        i = 0
        for resource, quantity in required_resources.items():
            self.agent.current_load[i] -= quantity
            self.map.rec_ent[resource] += quantity
            i += 1

    # Função que avalia a quantidade de recursos disponíveis no camião
    async def check_resources(self):
        total_load = 0
        for i in range (len(self.agent.current_load)):
            total_load += self.agent.current_load[i]
        if total_load < self.agent.vehicle_capacity * 0.2:
            time = self.get_distance(self.agent.depot_location)
            await asyncio.sleep(time)
            await self.reload_resources()

    # Função que reabastece numa base os recursos do camião
    async def reload_resources(self):
        time = 0.5
        await asyncio.sleep(time)
        for i in range (len(self.agent.resource_types)):
            self.agent.current_load[i] = self.agent.vehicle_capacity / len(self.agent.resource_types)

    # Função que define o comportamento cíclico de um Shelter Agent, que aguarda uma mensagem e depois age de acordo com o tipo de mensagem recebida
    # Chama a função que avalia os recursos do camião
    async def run(self):
        async with asyncio.Lock():
            await self.reload_resources()
            try:
                msg = await self.receive(timeout=1)
                if msg:
                    if msg.get_metadata("performative") != "disconfirm":
                        sender = str(msg.sender)
                        position = msg.get_metadata("position")
                        urgency = msg.get_metadata("urgency")
                        resources = msg.get_metadata("resources")
                        resources = ast.literal_eval(resources)
                        position = ast.literal_eval(position)
                        if msg.get_metadata("performative") == "request":
                            await self.send_proposal_message(position, urgency, resources, sender)
                        elif msg.get_metadata("performative") == "confirm":
                            print(msg.body)
                            time = self.get_distance(self.position) * 0.05  # 20 km/h
                            delay = random.randint(0, 3) * 0.05  # Estrada cortada
                            await asyncio.sleep(time + delay)
                            self.agent.current_location = self.position
                            await self.deliver_resources(resources, sender)
                            time = 0.5 #Tempo de entrega: meia hora
                            await asyncio.sleep(time)
            except Exception:
                pass
            await self.check_resources()
