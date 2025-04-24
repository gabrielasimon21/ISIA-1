import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import ast
import random

# Classe que representa os Shelter Agents
class ShelterAgent(Agent):
    def __init__(self, jid, password, number, location, capacity, environment, n_supply_agents):
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
        self.n_supply_agents = n_supply_agents

    # Função que inicia o comportamento cíclico dos Shelter Agents
    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        try:
            self.add_behaviour(ShelterRun(self, self.location, self.environment), template)
        except Exception as e:
            print(f"ERRO: {e}")

# Classe que representa o comportamento cíclico dos Shelter Agents
class ShelterRun(CyclicBehaviour):
    def __init__(self, agent, location, map):
        super().__init__()
        self.agent = agent
        self.location = location
        self.position = [0, 0]
        self.information = [0, 0]
        self.lock = asyncio.Lock()
        self.map = map

    # Função que envia mensagem ao agente civil a informar que foi alocado um agente para socorrer os civis a necessitar de abrigo da sua célula
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

    # Função que envia uma mensagem ao agente civil a informar que não existem agentes disponíveis neste momento para socorrer os civis a necessitar de abrigo da sua célula
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

    # Função que avalia as propostas enviadas no protocolo Contract Net com outros Shelter Agents
    # Responde com uma mensagem de confirmação ao agente com a melhor proposta (o que se encontra mais perto do pedido de socorro)
    # Responde com mensagens de desconfirmação a todos os outros agentes que enviaram propoposta e não foram escolhidos
    # Informa o civil do agente que foi escolhido para a sua célula (caso seja o caso)
    # Informa o civil que não foi possível atribuir nenhum agente à sua célula (caso seja o caso)
    async def respond_proposals(self, not_shelter, civil, propose_messages, position, informations):
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
            if not_shelter:
                await self.desconfirm_civil(civil, position)
            else:
                print(f"DESALOJAMENTO: Os civis do shelter {civil.jid} ficaram desalojados por falta de recursos")
                self.map.dados[8] -= self.agent.current_occupancy
                self.agent.current_occupancy = 0
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
                if not_shelter:
                    await self.confirm_civil(civil, best_agent)
            except Exception:
                if not_shelter:
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

    # Função que avalia a disponibilidade de um Shelter Agent receber x número de civis no seu abrigo
    def check_availability(self, civilians):
        return self.agent.current_occupancy + civilians <= self.agent.capacity

    # Função que envia uma proposta para outro agente que lhe enviou um request durante o protocolo Contract Net
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

    # Função que avalia o número de recursos do Shelter
    # Caso sejam necessários mais recursos, inicia um protocolo Contract Net com os Supply Agents
    async def check_resources(self):
        for resource, amount in self.agent.supply_status.items():
            if amount < (0.2 * self.agent.capacity):
                print(f"RECURSOS - {self.agent.jid}: {resource} está abaixo de 20%, pedido de mais")
                await self.contract_net_supply()
                break

    # Função que atualiza o número de recursos do shelter
    def update_resource_requirements(self):
        self.agent.resource_requirements["food"] = self.agent.current_occupancy * 2
        self.agent.resource_requirements["water"] = self.agent.current_occupancy * 3
        self.agent.resource_requirements["medical_supplies"] = self.agent.current_occupancy * 0.1
        self.update_urgency()

    # Função que inicia um protocolo Contract Net ao enviar a todos os Supply um request
    # Depois de enviados os requests, guarda as mensagens de propostas para serem analisadas
    async def contract_net_supply(self):
        self.update_resource_requirements()
        for i in range(1, self.agent.n_supply_agents):
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
        for i in range(self.agent.n_supply_agents):
            try:
                msg = await self.receive(timeout=1)
                if msg:
                    dest = str(msg.sender)
                if msg and msg.get_metadata("performative") == "propose" and not dest.startswith("shelter"):
                    propose_messages.append(msg)
            except Exception:
                pass
        await self.respond_proposals_supply(propose_messages)

    # Função que avalia as propostas enviadas no protocolo Contract Net com os Supply Agents
    # Responde com uma mensagem de confirmação ao agente com a melhor proposta (o que se encontra mais perto do pedido de socorro)
    # Responde com mensagens de desconfirmação a todos os outros agentes que enviaram propoposta e não foram escolhidos
    # Caso seja escolhido um agente, reabastece os seus recursos
    # Caso não seja escolhido um agente, inicia um rotocolo Contract Net para realojar os agentes civis do seu abrigo
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
            self.agent.environment.n_recusas += 1
            print(f"NEGAÇÃO SUPPLY: O Shelter agent {self.agent.jid} não conseguiu obter mais recursos")
            location = str(self.agent.current_location)
            occupancy = str (self.agent.current_occupancy)
            await self.contract_net(location, occupancy, False, self.agent)
        else:
            best_agent = str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            location = str(self.agent.location)
            urgency = str(self.agent.urgency_level)
            resources = str(self.agent.resource_requirements)
            msg.set_metadata("position", location)
            msg.set_metadata("urgency", urgency)
            msg.set_metadata("resources", resources)
            msg.body = f"REABASTECIMENTO: O agente escolhido para o shelter {self.agent.jid} foi o Supply Agent: {best_agent} e encontra-se à distância {max}km"
            try:
                await self.send(msg)
                await self.receive_resources()
            except Exception:
                pass
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

    # Função que avalia a urgência com que o Shelter Agent necessita de recursos
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

    # Função que simula o reabastecimento do abrigo
    async def receive_resources(self):
        for resource, quantity in self.agent.resource_requirements:
            self.agent.supply_status[resource] += quantity

    # Função que simula o tempo que demora a socorrer x civis a necessitar de abrigo
    def get_rescue_time(self, information):
        time = information * 0.05 #Resgate de 20 civis p/h
        return time

    # Função que calcula a distância a uma determinada célula afetada
    def get_distance(self, position):
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    # Função que gasta os recursos, de acordo com o número de ocupantes do abrigo
    def spend_resources(self):
        self.agent.supply_status['food'] -= self.agent.current_occupancy * 0.1
        self.agent.supply_status['water'] -= self.agent.current_occupancy * 0.1
        self.agent.supply_status['medical_supplies'] -= self.agent.current_occupancy * 0.01
        for resource in self.agent.supply_status:
            if self.agent.supply_status[resource] < 0:
                self.agent.supply_status[resource] = 0

    # Função que inicia um protocolo Contract Net ao enviar a todos os Shelter Agents um request
    # Depois de enviados os requests, guarda as mensagens de propostas para serem analisadas
    async def contract_net(self, position, information, civil, sender):
        for i in range(12):
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
        for i in range(11):
            try:
                msg = await self.receive(timeout=1)
                if msg:
                    dest = str(msg.sender)
                if msg and msg.get_metadata("performative") == "propose" and not dest.startswith("supply"):
                    shelter_propose_messages.append(msg)
            except Exception:
                pass
        await self.respond_proposals(civil, sender, shelter_propose_messages, position, information)

    # Função que define o comportamento cíclico de um Shelter Agent, que aguarda uma mensagem e depois age de acordo com o tipo de mensagem recebida
    # Chama a função que gasta os recursos do abrigo
    # Chama a função que avalia os recursos do abrigo
    async def run(self):
        async with self.lock:
            try:
                msg = await self.receive(timeout=1)
                if msg:
                    sender = str(msg.sender)
                    position = msg.get_metadata("value")
                    if msg.get_metadata("performative") == "inform":
                        print(msg.body)
                        information = msg.get_metadata("value2")
                        #CONTRACT NET
                        await self.contract_net(position, information, True, sender)
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
            except Exception:
                pass
        self.spend_resources()
        await self.check_resources()
