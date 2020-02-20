from .event import Event

class InvalidateEvent(Event): 
    def __init__(self, *UUIDs): 
        super().__init__(ts=0)
        self.ids = UUIDs 

    
    def execute(self): 
        super().execute()
        return {
            "ids": self.ids
        }
