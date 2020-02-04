from .event_process import EventProcess

class RequestEventProcess(EventProcess):
    def __init__(self, queue, id, distribution=None):
        super(RequestEventProcess, self).__init__()

    def run(self):
        '''
        Generates ride request events based on distributions
        '''
        while True:
            pass
