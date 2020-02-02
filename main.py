import multiprocessing as mp
import random
import time

from engine import Engine
from event_factory import EventFactory

def main():
    engine = Engine()
    queue = mp.Queue()

    processes = [EventFactory(queue, i) for i in range(2)]

    for p in processes:
        p.start()

    while True:
        event = queue.get()
        engine.schedule(event)

        engine.tick()

if __name__=="__main__":
    main()
