import asyncio
import spade
from async_timeout import timeout
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.behaviour import OneShotBehaviour
from spade.template import Template
import time

class ShelterAgent(Agent):
    def __init__(self, jid, password, location, capacity, environment):
        super().__init__(jid, password)
        self.location = location  
        self.capacity = capacity  
        self.current_occupancy = 0  
        self.resource_requirements = {"food": 0, "water": 0, "medical_supplies": 0} 
        self.supply_status = {"food": 0, "water": 0, "medical_supplies": 0}  
        self.urgency_level = 0  
        self.responder_status = {"incoming_civilians": 0, "estimated_arrival_time": None}  
        self.emergency_status = False 
        self.environment = environment 

    #class ShelterBehaviour(CyclicBehaviour):
        #async def run(self):
            #msg = await self.receive(timeout=10)
            #if msg:
                #instruction = eval(msg.body)
                #if instruction["type"] == "resource_delivery":
                    #await self.agent.receive_resources(instruction)
                #elif instruction["type"] == "incoming_civilians":
                    #await self.agent.coordinate_transport(instruction)
                #elif instruction["type"] == "emergency_status":
                    #await self.agent.emergency_management()
            #print("RecvBehav running")
            #msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            #if msg:
                #print("Message received with content: {}".format(msg.body))
            #else:
                #print("Did not received any message after 10 seconds")
        
    async def request_resources(self):
        self.resource_requirements["food"] = self.current_occupancy * 2
        self.resource_requirements["water"] = self.current_occupancy * 3 
        self.resource_requirements["medical_supplies"] = int(self.current_occupancy * 0.1)
        
        self.update_urgency()
        
        resource_request = {
            "type": "resource_request",
            "location": self.location,
            "urgency": self.urgency_level,
            "required_resources": self.resource_requirements
        }
        msg = Message(to="supply_vehicle_agent@localhost")
        msg.set_metadata("performative", "inform")
        msg.body = str(resource_request)
        await self.send(msg)
        print(f"Resource request sent: {resource_request}")

    async def receive_resources(self, instruction):
        delivered_resources = instruction["delivered_resources"]
        for resource, quantity in delivered_resources.items():
            self.supply_status[resource] += quantity
        print(f"Received resources: {delivered_resources}")
    
    async def coordinate_transport(self, instruction):
        incoming_civilians = instruction["incoming_civilians"]
        estimated_arrival_time = instruction["estimated_arrival_time"]
        
        self.responder_status["incoming_civilians"] = incoming_civilians
        self.responder_status["estimated_arrival_time"] = estimated_arrival_time

        await self.update_capacity(incoming_civilians)

    async def update_capacity(self, incoming_civilians):
        self.current_occupancy += incoming_civilians
        if self.current_occupancy > self.capacity:
            print("Shelter overcapacity! Triggering emergency response...")
            self.emergency_status = True
            await self.emergency_management()
        else:
            print(f"Updated shelter occupancy: {self.current_occupancy}/{self.capacity}")
    
    async def emergency_management(self):
        if self.current_occupancy > self.capacity:
            print(f"Overcapacity! Current occupancy: {self.current_occupancy}, Capacity: {self.capacity}")
            await self.communicate_with_other_shelters()
        if self.supply_status["medical_supplies"] == 0:
            print("Critical shortage of medical supplies! Increasing urgency of request.")
            self.urgency_level = 5 
    
    #async def communicate_with_other_shelters(self):
        #msg = Message(to="neighbor_shelter_agent@localhost")
        #msg.set_metadata("performative", "inform")
        #msg.body = f"Shelter at {self.location} is overcapacity. Can you accommodate {self.current_occupancy - self.capacity} civilians?"
        #await self.send(msg)
        #print(f"Sent request to neighbor shelter: {msg.body}")

    def update_urgency(self):
        food_shortage = self.resource_requirements["food"] - self.supply_status["food"]
        water_shortage = self.resource_requirements["water"] - self.supply_status["water"]
        medical_shortage = self.resource_requirements["medical_supplies"] - self.supply_status["medical_supplies"]

        if food_shortage > 0 or water_shortage > 0 or medical_shortage > 0:
            self.urgency_level = max(food_shortage, water_shortage, medical_shortage)
            print(f"Urgency updated to {self.urgency_level}")
        else:
            self.urgency_level = 0
            print("Resources are adequate; urgency set to 0.")
    
    async def predictive_resource_management(self):
        projected_occupancy = self.current_occupancy + self.responder_status["incoming_civilians"]
        self.resource_requirements["food"] = projected_occupancy * 2
        self.resource_requirements["water"] = projected_occupancy * 3
        self.resource_requirements["medical_supplies"] = int(projected_occupancy * 0.1)

        await self.request_resources()

    async def setup(self):
        template = Template(metadata={"performative": "inform", "ontology": "myOntology", "language": "OWL-S"})
        self.add_behaviour(ReceiveBehav(), template)

class ReceiveBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=5)
        if msg:
            print(f"Received message: {msg.body}")







