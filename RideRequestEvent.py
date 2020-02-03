class RideRequestEvent(Event):

    def __init__(self, rider, ts=None, *args, **kwargs):
        super().__init__()



    def execute(self):
        print(self.rider)
