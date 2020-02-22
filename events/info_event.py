from .event import Event

class NumRidesEvent(Event):
	def __init__(self,ts,num_rides):
		super().__init__(ts=ts)
		self.num_rides = num_rides

	def execute(self):
		return self.num_rides


class NumBusesEvent(Event):

	def __init__(self,ts,num_buses):
		super().__init__(ts=ts)
		self.num_buses = num_buses

	def execute(self):
		return self.num_buses

class BusCapacityEvent(Event):
	def __init__(self,ts,bus_capacity):
		super().__init__(ts=ts)
		self.bus_capacity = bus_capacity

	def execute(self):
		return self.bus_capacity