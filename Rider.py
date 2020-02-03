class Rider:

    def __init__(self, id, startTAZ, endTAZ):
        self.id = id
        self.start = startTAZ
        self.end = endTAZ

    def requested(ts):
        self.request_ts = ts

    def pickedUp(ts):
        self.pickup_ts = ts

    def droppedOff(ts):
        self.dropoff_ts = ts

    def __str__(self):
        # Can be used for logging #
        if self.dropoff_ts is not None:
            return "Rider {} was dropped off at {}.".format(self.id, self.dropoff_ts)
        elif self.pickup_ts is not None:
            return "Rider {} was picked up at {}.".format(self.id, self.pickup_ts)
        elif self.request_ts is not None:
            return "Rider {} request ride at {}.".format(self.id, self.request_ts)
        else:
            return ""

    def __repr__(self):
        # Can be used to store into db #
        return {"ID":self.id, "Start":self.start, "End":self.end, "Request TS": self.request_ts, "Pickup TS": self.pickup_ts, "Dropoff TS": self.dropoff_ts}
