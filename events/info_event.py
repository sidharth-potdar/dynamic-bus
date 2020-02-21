from .event import Event

class NumRidesEvent(Event):

	def __init__(self,ts,num_rides):
		super(Event, self).__init__(ts)
		self.num_rides = num_rides

	def execute(self):
		return num_rides


class NumBusesEvent(Event):

	def __init__(self,ts,num_buses):
		super(Event, self).__init__(ts)
		self.num_buses = num_buses

	def execute(self):
		return num_buses

class BusCapacityEvent(Event):
	def __init__(self,ts,bus_capacity):
		super(Event, self).__init__(ts)
		self.bus_capacity = bus_capacity

	def execute(self):
		return self.bus_capacity