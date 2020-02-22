from .event import Event

class EndScheduleEvent(Event): 
    def __init__(self, id): 
        super().__init__()
        self.id = id 
    def execute(self, id):
        return super().execute()
        