from .event import Event

class EndScheduleEvent(Event): 
    def execute(self):
        return super().execute()
        