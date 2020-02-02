from event_process import EventProcess

class RideRequestEventProcess(Process):
    def __init__(self, queue, id, distribution=None):
        super(RideRequestEventProcess, self).__init__()

    def run(self):
        '''
        Generates ride request events based on distributions
        '''
        while True:
            pass
