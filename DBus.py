
class DBus:

    def __init__(self, startTAZ, capacity = 6, *args, **kwargs):
        self.currentLoc = startTAZ

        # capacity is the maximum number of people a bus can seat
        # load refers to the number of people currently in the bus
        self.capacity = capacity
        self.load = 0


    def addRider(self):
        if self.load == self.capacity:
            return False
        else:
            self.load += 1
            return True

    def deleteRider(self):
        if self.load == 0:
            return False
        else:
            self.load -= 1
            return True


    def getCurrentPosition(self):
        return self.currentLoc

    def isFull(self):
        return self.load == self.capacity

    def isEmpty(self):
        return self.load == 0
