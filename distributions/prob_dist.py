import random
import csv
from operator import itemgetter


def generateRides(multiplier=1):
    with open('distributions/ride_volume.csv','r') as ridef:
        ride_reader = csv.reader(ridef)
        next(ride_reader) # IGNORE HEADER
        binning = []
        ride_probs = []

        for row in ride_reader:
            bin_start, ride_num_probability = row
            bin_start = int(bin_start)
            ride_num_probability = float(ride_num_probability)

            binning.append(bin_start)
            ride_probs.append(ride_num_probability)


    bin_width = binning[1] - binning[0]

    num_rides = random.choices(population=binning, weights=ride_probs, k=1)[0]
    num_rides += random.randint(0, bin_width) # force the idea of picking from a range instead of picking an exact number of events from data

    num_rides *= multiplier
    print(num_rides)

    from_to_ct = []
    ride_hr = []

    fth = []
    probs = []

    with open('distributions/joint_probability.csv','r') as jpf:
        jpreader = csv.reader(jpf)
        next(jpreader) # IGNORE HEADER
        for row in jpreader:
            from_to_hr_str, probability = row # Formatted as ((from_ct, to_ct), hr) probability
            probability = float(probability)
            from_to_hr_str = from_to_hr_str[1:-1] # ignore outer parentheses
            hr = int(from_to_hr_str[-1]) # get hr
            from_ct, to_ct = from_to_hr_str[1:-4].split(',') # ignore hr space comma and inner parens
            from_ct = from_ct.strip()
            to_ct = to_ct.strip()
            hr += random.random()
            fth.append((from_ct,to_ct,hr))
            probs.append(probability)


    generated_rides = random.choices(population=fth, weights=probs, k=num_rides)
    generated_rides.sort(key=itemgetter(2))
    return generated_rides
