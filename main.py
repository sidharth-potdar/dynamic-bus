import multiprocessing as mp
import random
import time

from engine import Engine
from event_processes import EventProcess

def main():
    engine = Engine()
    queue = mp.Queue()

    processes = [EventProcess(queue, i) for i in range(2)]

    for p in processes:
        p.start()

    while True:
        event = queue.get()
        engine.schedule(event)

        engine.tick()

if __name__=="__main__":
    main()
