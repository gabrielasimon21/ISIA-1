import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import time
import heapq  

class SupplyVehicleAgent(Agent):
    def __init__(self, jid, password, depot_location, vehicle_capacity, resource_types, environment):
        super().__init__(jid, password)
        self.depot_location = depot_location  
        self.vehicle_capacity = vehicle_capacity 
        self.resource_types = resource_types  # List of resources (food, water, medical supplies)
        self.current_load = {}  
        self.affected_regions = [] 
        self.road_conditions = {}  
        self.priority_levels = {} 
        self.environment = environment 
        
    class SupplyVehicleBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg: 
                instruction = eval(msg.body)
                if instruction["type"] == "delivery_request":
                    await self.handle_delivery_request(instruction)
                elif instruction["type"] == "emergency_route_adjustment":
                    await self.handle_emergency_adjustment(instruction)
        
        async def handle_delivery_request(self, instruction):
            region = instruction["region"]
            resources_needed = instruction["resources_needed"]
            priority = instruction["priority"]
            self.agent.affected_regions.append({"region": region, "resources_needed": resources_needed, "priority": priority})
            self.agent.priority_levels[region] = priority
            await self.agent.load_balance()
            await self.agent.delivery_schedule()
        
        async def handle_emergency_adjustment(self, instruction):
            new_condition = instruction["road_condition"]
            self.agent.road_conditions[instruction["region"]] = new_condition
            await self.agent.route_optimization()  

    async def route_optimization(self):
        graph = self.environment.get_road_network()
        start = self.depot_location
        destinations = [region["region"] for region in self.affected_regions]
        best_route = self.dijkstra(graph, start, destinations)
        print(f"Optimized route: {best_route}")
    
    def dijkstra(self, graph, start, destinations):
        queue = [(0, start)]
        visited = set()
        distances = {start: 0}
        while queue:
            (cost, node) = heapq.heappop(queue)
            if node in visited:
                continue
            visited.add(node)
            for neighbor, weight in graph[node]:
                if neighbor in visited:
                    continue
                new_cost = cost + weight
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
        return distances
    
    async def load_balance(self):
        total_load = sum(self.current_load.values())
        if total_load > self.vehicle_capacity:
            print("Load exceeds capacity! Adjusting...")
        else:
            print("Load balanced within capacity.")
    
    async def delivery_schedule(self):
        sorted_regions = sorted(self.affected_regions, key=lambda x: (x["priority"], self.road_conditions.get(x["region"], "clear")))
        for region in sorted_regions:
            await self.deliver_resources(region)
    
    async def deliver_resources(self, region):
        resources_needed = region["resources_needed"]
        for resource, quantity in resources_needed.items():
            if self.current_load.get(resource, 0) >= quantity:
                print(f"Delivering {quantity} of {resource} to {region['region']}")
                self.current_load[resource] -= quantity
            else:
                print(f"Insufficient {resource} to deliver to {region['region']}")
    
    async def return_to_depot(self):
        print(f"Returning to depot at {self.depot_location} for refuel/reload.")
        await asyncio.sleep(1)
    
    async def communicate_with_other_agents(self):
        msg = Message(to="another_agent@localhost")
        msg.set_metadata("performative", "inform")
        msg.body = "Supply vehicle agent reporting status."
        await self.send(msg)
