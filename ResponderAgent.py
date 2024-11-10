import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import ast


class ResponderAgent(Agent):
    def __init__(self, jid, password, number, current_location, environment):
        super().__init__(jid, password)
        self.number = number
        self.current_location = current_location
        self.busy = False
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
            msg.body = f"CONTRACT NET: O agente escolhido para a célula {position} foi o Responder Agent: {best_agent} e encontra-se à distância {max}km"
            print(msg.body)
            try:
                await self.send(msg)
            except Exception as e:
                await self.desconfirm_civil(civil, position)
                exception = True
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
                    except Exception as e:
                        pass
            if not exception:
                informations = ast.literal_eval(informations)
                self.map.dados[6] += informations[0]
                self.map.dados[7] += informations[1]
                await self.confirm_civil(civil, best_agent, max)

    async def confirm_civil(self, civil, agent, dist):
        msg = Message(to=civil)
        msg.set_metadata("performative", "confirm")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"O agente escolhido para a sua célula foi o Responder Agent: {agent} e encontra-se à distância {dist}km"
        try:
            await self.send(msg)
        except Exception:
            pass

    async def desconfirm_civil(self, civil, position):
        msg = Message(to=civil)
        msg.set_metadata("performative", "desconfirm")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"Neste momento não é possível atribuir um agente à sua célula"
        try:
            await self.send(msg)
        except Exception as e:
            pass
        print(f"NEGAÇÂO: Não existem agentes disponíveis no momento para a célula {position}")


    async def send_reject_message(self, agent):
        msg = Message(to=agent)
        msg.set_metadata("performative", "reject")
        msg.set_metadata("ontology", "myOntology")
        msg.set_metadata("language", "OWL-S")
        msg.body = f"Request rejected: Agent busy"
        try:
            await self.send(msg)
        except Exception as e:
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
        except Exception as e:
            pass

    def get_rescue_time(self, information):
        time = information[0] * 0.1 + information [1] * 0.1 #Resgate de 10 feridos e 10 mortos p/h
        return time

    async def respond_time(self, position, information):
        time = self.get_distance(position) * 0.05 #20 km/h
        await asyncio.sleep(time)
        self.agent.current_location = position
        time = self.get_rescue_time(information)
        await asyncio.sleep(time)
        self.agent_busy = False


    async def run(self):
        async with self.lock:
            msg = await self.receive(timeout=1)
            if msg:
                sender = str(msg.sender)
                position = msg.get_metadata("value")
                if msg.get_metadata("performative") == "inform":
                    print(f"INFORMAÇÃO: {msg.body}")
                    information = msg.get_metadata("value2")
                    self.position = ast.literal_eval(position)
                    self.information = ast.literal_eval(information)
                    if not self.agent.busy:
                        self.agent.busy = True
                        distance = self.get_distance(self.position)
                        await self.confirm_civil(sender, self.agent, distance)
                        print(f"CONTACTO DIRETO: O agente escolhido para a célula {self.position} foi o Responder Agent: {self.agent.jid}, e encontra-se à distância {distance}km")
                        self.map.dados[6] += self.information[0]
                        self.map.dados[7] += self.information[1]
                    else: #CONTRACT NET
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
                                except Exception as e:
                                    pass
                        propose_messages = []
                        for i in range(19):
                            msg = await self.receive(timeout=1)
                            if msg and msg.get_metadata("performative") == "propose":
                                propose_messages.append(msg)
                        await self.respond_proposals(sender, propose_messages, position, information)
                elif msg.get_metadata("performative") == "request":
                    position = ast.literal_eval(position)
                    if self.agent.busy:
                        await self.send_reject_message(sender)
                    else:
                        await self.send_proposal_message(sender, position)
                elif msg.get_metadata("performative") == "confirm":
                    self.agent.busy = True
                    information = msg.get_metadata("value2")
                    self.position = ast.literal_eval(position)
                    self.information = ast.literal_eval(information)
            if self.agent.busy:
                await self.respond_time(self.position, self.information)






