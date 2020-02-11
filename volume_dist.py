import csv
import itertools

def generateDistributions():

    pickup_dist = {}
    dropoff_dist = {}

    with open('trip_stats_taz_0.csv') as tripcsv:
        tripreader = csv.reader(tripcsv)
        next(tripreader)
        num_taz = 0

        for row in tripreader:
            taz, dow, hr, pickups, dropoffs = row
            num_taz += 1

            taz = int(taz)
            dow = int(dow)
            hr = int(hr) - 3 # Because indexing starts from 3AM and goes on to 2 AM
            # Subtracting 3 resets it 00:00 as 12 AM which is conventional

            pair = (dow, hr)
            if pair in pickup_dist.keys():
                pickup_dist[pair][taz] = float(pickups)
            else:
                pickup_dist[pair] = {}
                pickup_dist[pair][taz] = float(pickups)


            if pair in dropoff_dist.keys():
                dropoff_dist[pair][taz] = float(dropoffs)
            else:
                dropoff_dist[pair] = {}
                dropoff_dist[pair][taz] = float(dropoffs)


        dow_vals = [i for i in range(7)]
        hr_vals = [i for i in range(24)]

        for pair in itertools.product(dow_vals, hr_vals):
            pair = tuple(pair)

            num_pickups = sum(pickup_dist[pair].values())
            num_dropoffs = sum(dropoff_dist[pair].values())

            pickup_dist[pair] = {k: v / num_pickups for k, v in sorted(pickup_dist[pair].items(), key=lambda item: item[1])}

            dropoff_dist[pair] = {k: v / num_dropoffs for k, v in sorted(dropoff_dist[pair].items(), key=lambda item: item[1])}





    return pickup_dist, dropoff_dist



