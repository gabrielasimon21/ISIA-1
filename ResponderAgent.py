import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import time

class ResponderAgent(Agent):
    def __init__(self, jid, password, current_location, vehicle_capacity, environment):
        super().__init__(jid, password)
        self.current_location = current_location
        self.vehicle_capacity = vehicle_capacity
        self.vacant_seats = vehicle_capacity
        self.status = "available"  # "available" or "busy"
        self.environment = environment

    class ResponderBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                instruction = eval(msg.body)
                if instruction["type"] == "rescue_request":
                    await self.agent.receive_call_from_civilian(instruction)
                elif instruction["type"] == "responder_request":
                    await self.agent.receive_call_from_other_agent(instruction)
                elif instruction["type"] == "availability_response":
                    await self.agent.process_availability_response(instruction)

    async def receive_call_from_civilian(self, instruction):
        civilians = instruction["number_of_civilians"]
        location = instruction["location"]
        civilian_jid = instruction["civilian_jid"]
        print(f"Received rescue request from civilians at {location} for {civilians} people.")
        await self.check_availability()
        if self.status == "available" and self.vacant_seats >= civilians:
            await self.respond_to_civilian(civilian_jid, "confirmed")
            await self.move_to_call_location(location)
            await self.transport_civilians_to_shelter(civilians)
        else:
            await self.respond_to_civilian(civilian_jid, "pending")
            await self.assign_other_agent(instruction)

    async def receive_call_from_other_agent(self, instruction):
        civilians = instruction["number_of_civilians"]
        location = instruction["location"]
        requesting_agent_jid = instruction["agent_jid"]
        print(f"Received request from another responder agent to assist with {civilians} civilians at {location}.")
        await self.check_availability()
        if self.status == "available" and self.vacant_seats >= civilians:
            await self.respond_to_agent(requesting_agent_jid, "available")
            await self.move_to_call_location(location)
            await self.transport_civilians_to_shelter(civilians)
        else:
            await self.respond_to_agent(requesting_agent_jid, "unavailable")

    async def process_availability_response(self, instruction):
        response = instruction["response"]
        agent_jid = instruction["agent_jid"]
        if response == "available":
            print(f"Agent {agent_jid} is available and will handle the request.")
        else:
            print(f"Agent {agent_jid} is unavailable.")
            # If no agents are available, you might need to notify civilians or take other actions.

    async def check_availability(self):
        if self.vacant_seats > 0:
            self.status = "available"
        else:
            self.status = "busy"

    async def respond_to_civilian(self, civilian_jid, response):
        msg = Message(to=civilian_jid)
        msg.set_metadata("performative", "inform")
        msg.body = str({"type": "rescue_response", "response": response})
        await self.send(msg)
        print(f"Sent response to civilian {civilian_jid}: {response}")

    async def respond_to_agent(self, agent_jid, response):
        msg = Message(to=agent_jid)
        msg.set_metadata("performative", "inform")
        msg.body = str({"type": "availability_response", "response": response, "agent_jid": str(self.jid)})
        await self.send(msg)
        print(f"Sent availability response to agent {agent_jid}: {response}")

    async def move_to_call_location(self, location):
        print(f"Moving from {self.current_location} to location {location}...")
        # Simulate movement
        await asyncio.sleep(1)
        self.current_location = location
        print(f"Arrived at location {location}.")

    async def transport_civilians_to_shelter(self, civilians):
        print(f"Transporting {civilians} civilians to shelter...")
        if self.vacant_seats >= civilians:
            self.vacant_seats -= civilians
            # Simulate transport
            await asyncio.sleep(1)
            print(f"Transported {civilians} civilians to shelter.")
            # After dropping off, update vacant seats
            self.vacant_seats += civilians
            print(f"Vacant seats available: {self.vacant_seats}")
        else:
            print(f"Not enough seats to transport {civilians} civilians.")
        self.status = "available"

    async def assign_other_agent(self, instruction):
        print("Attempting to assign another agent to handle the request.")
        other_agents = self.environment.get_other_responder_agents(self.jid)
        assigned = False
        for agent_jid in other_agents:
            msg = Message(to=agent_jid)
            msg.set_metadata("performative", "request")
            msg.body = str({
                "type": "responder_request",
                "number_of_civilians": instruction["number_of_civilians"],
                "location": instruction["location"],
                "agent_jid": str(self.jid)
            })
            await self.send(msg)
            # Wait for immediate response
            await asyncio.sleep(0.1)
            assigned = True
        if not assigned:
            civilian_jid = instruction["civilian_jid"]
            await self.respond_to_civilian(civilian_jid, "denied")
            print("No available agents to assign. Denied request to civilian.")

    def setup(self):
        b = self.ResponderBehaviour()
        self.add_behaviour(b)