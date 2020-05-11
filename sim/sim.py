import numpy as np
from .station import Station
from .consts import *

class Simulation:
    """
    The primary controller class for the bike share simulation.

        Method start begins the simulation.

        Method update triggers bike movements.
    
    Let's start off simple simulation by making a 60-min simulation.
    - Every minute, there's a probability of a bike being checked out from
      a station.
    - When a bike is checked out, we decide which open station it'll go to. That
      will determine how long it'll take. We then put that bike on hold until
      the minute where it should land.
    - When the simulation is over, compile all logs and print them out to a 
      JSON file.
    """
    def __init__(self, length, size = None):
        """
        Sets up the stations and initializes the simulation.

        Parameters
        ----------
        length: [int] the duration in minutes that the sim will last.

        size: [str] (optional) will determine the size of the simulation. To 
              be defined later.
        """
        self.stations = [
            Station(0, (0, 0), 1, 1, 0),
            Station(1, (1, 1), 1, 1, 1)
        ]
        self.bikes_in_transit = []
        
        self.print_start(length)
        self.run(length)
        

    def print_start(self, length):
        """
        This prints out the block of text that displays at the top of the
        output of the simulation.
        """
        message = f'This bike share system has {len(self.stations)} stations:'
        thick_divider = '=' * len(message)
        thin_divider = '-' * len(message)

        print('\n')
        print(thick_divider)
        print('INITIALIZING SIMULATION')
        print(thin_divider)
        print(f'This bike share system has {len(self.stations)} stations:')
        for station in self.stations:
            print('Station:', station.id, 
                  'Docks:', len(station.docks),
                  'Bikes:', station.available_bikes)
        print('\n')
        print(f'The simulation will cover {length} minutes')
        print(thin_divider)
    
    def run(self, length):
        """
        Runs the simulation.
        """
        potential_checkouts = self.generate_checkouts(
            length, self.poisson_thresh)

        # Each loop represents one minute in the simulation    
        for i, potential_checkout in enumerate(potential_checkouts):
            print(f'Minute:', i+1)
            # If the potential checkout is true, let's check a bike out
            if potential_checkout:
                i = self.get_available_station('check out')
                print(f'---- Bike checked out of Station {self.stations[i].id}')
    
    ### HELPER FUNCTIONS ###

    def poisson_thresh(self, k):
        """
        Returns
        -------
        The threshold below which a random number between 1-100 must be to trigger a 
        bike ride. This is 100 * the probability of a Poisson process occuring with 
        given k and lambda values.
        
        Parameters
        -----------
        k: [int] Number of bikes being checked out within given checkout rate.

        lam: [int | float] Rate at which bikes are checked out (bikes/minute).
        """
        num = (LAMBDA ** k) * (np.math.exp(-LAMBDA))
        den = np.math.factorial(k)
        return (num / den) * 100

    def generate_checkouts(self, length, func):
        """
        Returns
        -------
        A numpy array of LENGTH elements, each element representing a bike 
        share event. Each element is True or False signifying whether or not a 
        bike will be checked out.

        This generates a bunch of k values using a normal distribution with mu = 0
        and sigma = 1. The distribution is modified by taking its absolute value
        and then shifting right by 1. All numbers are cast to int to be passed
        into factorial function later.

        Each k value is converted to a poisson probability and then multiplied by 
        100 (all by the vectorized poisson threshold function passed in as the 
        `func` parameter).

        Lastly, we generate LENGTH random integers from 1-100. For each element in 
        the checkout_thresholds, if the corresponding random integer is smaller than that threshold, we say that a bike is withdrawn.

        Parameters
        ----------
		length: [int] Length of simulation in minutes.

        func: [python function] The poisson threshold function. Must be passed 
		in as an argument to vectorize.
        """
        # The k values for which a poisson probability of occurrence is calculated.
        ks = np.random.normal(1, 1, length)
        ks = abs(ks) + 1
        ks = ks.astype(int)

        # Vectorize poisson threshold function and apply on ks
        poisson_thresh = np.vectorize(func, otypes = ['int'])
        checkout_thresholds = poisson_thresh(ks)

        # Values to check each probability against
        test_values = np.random.randint(1, 101, length)

        # The test values are lower than the threshold, a bike is checked out
        checkouts = checkout_thresholds >= test_values
        
        return checkouts
    
    def get_available_station(self, availability):
        """
        Returns
        -------
        Randomly selected list index of a station with at least one available 
        bike or one available dock. Random so as to not always pick same 
        stations from the list.

        Parameters
        ----------
        availability: [str] Either 'check in' or 'check out'
        """
        num_stations = len(self.stations)
        random_indexes = np.arange(0, num_stations)
        np.random.shuffle(random_indexes)

        for i in random_indexes:
            if (availability == 'check out') and (self.stations[i].available_bikes):
                return i
            elif (availability == 'check in') and (self.stations[i].available_docks):
                return i



# For every minute in the simulation:
# First, pick a k from a modified normal distribution. 
# Second, uses that k to calculate prob of k bikes being checked out
# Third, picks a number randomly between 0 and 100. If the number is within 
#     the percentage range, then those number of bikes are checked out that
#     minute.
# # For every bike checked out:
# # First, pick a random station
# # Second, see if that station has open bikes
# # Third, pick a destination from any of the other bikes and calculate time 
# #     based on 10 mph average speed. Put this bike "on hold" until time to 
# #     dock.
# # Fourth, if that station is full at docking time, find closest station with 
# # open slots and repeat third step until we can dock. Calculate price and 
# # store in log.