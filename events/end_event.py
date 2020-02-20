from .event import Event

class EndEvent(Event):
	
	def __init__(self,ts=None, current_ts=None,priority=11):
		super(EndEvent, self).__init__(ts=ts, current_ts=current_ts)
		self.priority = priority

	def execute(self):
		return {}
