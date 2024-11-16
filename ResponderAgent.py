import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import ast
import random


# Classe que representa os Responder Agents
class ResponderAgent(Agent):
    def __init__(self, jid, password, number, current_location, environment):
        super().__init__(jid, password)
        self.number = number
        self.current_location = current_location
        self.environment = environment

    # Função que inicia o comportamento cíclico dos Responder Agents
    async def setup(self):
        template = Template(metadata={"ontology": "myOntology", "language": "OWL-S"})
        try:
            self.add_behaviour(ResponderRun(self, self.current_location, self.environment), template)
        except Exception as e:
            print(f"ERRO: {e}")

# Classe que representa o comportamento cíclico dos Responder Agents
class ResponderRun(CyclicBehaviour):
    def __init__(self, agent, location, map):
        super().__init__()
        self.agent = agent
        self.location = location
        self.position = [0, 0]
        self.information = [0, 0]
        self.lock = asyncio.Lock()
        self.map = map

    # Função que avalia as propostas enviadas no protocolo Contract Net
    # Responde com uma mensagem de confirmação ao agente com a melhor proposta (o que se encontra mais perto do pedido de socorro)
    # Responde com mensagens de desconfirmação a todos os outros agentes que enviaram propoposta e não foram escolhidos
    # Informa o civil do agente que foi escolhido para a sua célula (caso seja o caso)
    # Informa o civil que não foi possível atribuir nenhum agente à sua célula (caso seja o caso)
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
            best_agent=str(best_agent)
            msg = Message(to=best_agent)
            msg.set_metadata("performative", "confirm")
            msg.set_metadata("ontology", "myOntology")
            msg.set_metadata("language", "OWL-S")
            msg.set_metadata("value", position)
            msg.set_metadata("value2", informations)
            msg.body = f"ALOCAÇÃO RESPONDER: O agente escolhido para a célula {position} foi o Responder Agent: {best_agent} e encontra-se à distância {max}km"
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


    # Função que envia mensagem ao agente civil a informar que foi alocado um agente para socorrer os mortos e feridos da sua célula
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

    # Função que envia uma mensagem ao agente civil a informar que não existem agentes disponíveis neste momento para socorrer os mortos e feridos da sua célula
    async def desconfirm_civil(self, civil, position):
        msg = Message(to=civil)
        msg.set_metadata("performative", "desconfirm")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"NEGAÇÃO RESPONDER: Não existem agentes disponíveis no momento para a célula {position}"
        try:
            await self.send(msg)
        except Exception:
            pass

    # Função que rejeita um request de outro agente no portocolo ContractNet por o agente se encontrar ocupado
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

    # Função que calcula a distância de um agente a uma determinada célula
    def get_distance(self, position):
        x = position[0]
        y = position[1]
        w = self.location[0]
        z = self.location[1]
        return abs(x-w) + abs (y-z)

    # Função que envia uma proposta para outro agente que lhe enviou um request durante o protocolo Contract Net
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

    # Função que simula o tempo demorado por um agente no resgate de uma determinada célula
    def get_rescue_time(self, information):
        time = information[0] * 0.1 + information [1] * 0.1 #Resgate de 10 feridos e 10 mortos p/h
        return time

    # Função que inicia um protocolo Contract Net ao enviar a todos os Responder Agents um request
    # Depois de enviados os requests, guarda as mensagens de propostas para serem analisadas
    async def contract_net(self, sender, position, information):
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
            try:
                msg = await self.receive(timeout=1)
                if msg and msg.get_metadata("performative") == "propose":
                    propose_messages.append(msg)
            except Exception:
                pass
        await self.respond_proposals(sender, propose_messages, position, information)

    # Função que define o comportamento cíclico de um Responder Agent, que aguarda uma mensagem e depois age de acordo com o tipo de mensagem recebida
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
                        await self.contract_net(sender, position, information)
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
            except Exception:
                pass





