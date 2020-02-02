class Scheduler:
    buses = []
    ride_statuses = {}

    def register(*events):
        '''
        Given a variable number of ride request events, handle them according to current state
        '''
        pass

    def find_nearest_bus(request_location):
        '''
        Find nearest bus to request location
        '''
        pass

    def assign_ride(ride_request):
        '''
        Given a ride request, assign it to a bus according to scheduler's policy
        '''
        pass
