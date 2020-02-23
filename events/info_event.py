from .event import Event

class NumRidesEvent(Event):
	def __init__(self,ts,num_rides):
		super().__init__(ts=ts)
		self.num_rides = num_rides

	def execute(self):
		return self.num_rides


class NumBusesEvent(Event):
	def __init__(self,ts,num_buses, origin_ride_id, new_bus_id, location):
		super().__init__(ts=ts)
		self.num_buses = num_buses
		self.origin_ride_id = origin_ride_id
		self.new_bus_id = new_bus_id
		self.location = location

	def execute(self):
		return self.num_buses
		
	def __repr__(self): 
		return f"(0,'{self.origin_ride_id}',{self.getExecutionPoint()},{self.location},{self.num_buses},{self.new_bus_id})"


class BusCapacityEvent(Event):
	def __init__(self,ts,bus_capacity):
		super().__init__(ts=ts)
		self.bus_capacity = bus_capacity

	def execute(self):
		return self.bus_capacity