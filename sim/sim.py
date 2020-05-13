import numpy as np
from scipy.spatial.distance import cityblock
from pprint import pprint as pp
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
        self.station_init()
        self.bikes_in_transit = []
        self.bikes_to_dock = []
        self.print_start(length)
        self.run(length)
        self.print_end()

    def station_init(self):
        """
        Sets up the stations for this simulation. Number of stations, size of
        stations, and number of bikes can be set from consts.py
        """
        bikes_per_station = NUM_BIKES // NUM_STATIONS

        station_id = 0
        bike_id = 0
        stations = []
        for _ in range(NUM_STATIONS):
            stations.append(Station(
                station_id, 
                LOCATIONS[station_id], 
                MEDIUM_STATION,
                bikes_per_station,
                bike_id
            ))
            station_id += 1
            bike_id += bikes_per_station

        self.stations = stations

    def run(self, length):
        """
        Runs the simulation.
        """
        potential_checkouts = self.generate_checkouts(
            length, self.poisson_thresh
        )

        # Each loop represents one minute in the simulation    
        for time, potential_checkout in enumerate(potential_checkouts):
            print(f'Minute:', time)

            if potential_checkout:

                # Could be more than one checkout this minute, make sure we 
                # get all of them
                for _ in range(potential_checkout):
                    self.check_out_sequence(time)
            
            if self.bikes_to_dock:
                self.check_in_sequence(time)
            
            self.update_bikes_in_transit()
    
    def check_out_sequence(self, time):
        """
        Performs a check-out sequence. 
        
        Checks for available stations. If exists, finds available dock and 
        then checks out the bike. If not exists, prints that no bikes were 
        available at this time.

        If bike was checked out, it is added to bikes in transit list.

        Parameters
        -----------
        time: [int] the minute that the current simulation is at.
        """
        station_id = self.get_available_station('check out')
        print('---- Customer tried to check out a bike')
        
        # Only proceed if there exists an open dock
        if station_id != None:

            # print('----', self.stations[station_id].available_bikes,
            #     'bike(s) available')

            # Find index of an open dock at this station and check out
            dock_id = self.get_available_dock(
                self.stations[station_id], 'check out'
            )

            bike = self.stations[station_id].docks[dock_id].check_out(time)
            end_station_id = self.determine_destination(station_id)
            duration = self.determine_trip_duration(
                station_id, end_station_id
            )

            # Add that bike to the in_transit list
            self.bikes_in_transit.append({
                'bike': bike, 
                'destination': end_station_id,
                'time_left': duration
            })

            print(f'---- Bike checked out of Station: {station_id} Dock: {dock_id}')
        
        else:
            print('---- No available stations for checkout at this time')
    
    def check_in_sequence(self, time):
        """
        Performs a check-in sequence.

        There are two possibilites: the original destination is open when the
        bike "arrives", or it isn't Both are covered here.
        """
        for bike in self.bikes_to_dock:

            print('---- Customer tried to check in a bike')

            destination_id = bike['destination']
            dock_id = self.get_available_dock(
                self.stations[destination_id], 'check in'
            )
            # Station is open
            if dock_id != None:
                self.stations[destination_id].docks[dock_id].check_in(
                    bike['bike'], time
                )
                print(
                    '---- Bike checked into Station:', destination_id,
                    'Dock:', dock_id
                )
            
            # Station isn't open. Pick another station and go there. The origin 
            # for this new trip is now the old destination (destination_id)
            else:
                print('---- Station was full. Customer could not check bike in')
                print('---- Setting off to find another station with empty slots')
                end_station_id = self.determine_destination(destination_id)
                duration = self.determine_trip_duration(
                    destination_id, end_station_id
                )

                # Add that bike to the in_transit list
                self.bikes_in_transit.append({
                    'bike': bike['bike'],
                    'destination': end_station_id,
                    'time_left': duration
                })
        self.bikes_to_dock = []
    
    def update_bikes_in_transit(self):
        """
        Updates self.bikes_in_transit by lowering the 'time_left' key by 1 
        every minute of the simulation.

        If a bike in transit has 'time_left' = 0, then that bike is moved to 
        self.bikes_to_dock.
        """
        updated_bikes_in_transit = []
        for bike in self.bikes_in_transit:
            bike['time_left'] -= 1
            if bike['time_left'] == 0:
                self.bikes_to_dock.append(bike)
            elif bike['time_left'] > 0:
                updated_bikes_in_transit.append(bike)
            else:
                raise ValueError(bike, 'Has negative time left')
        self.bikes_in_transit = updated_bikes_in_transit

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
    
    def print_end(self):
        """
        This prints out the block of text that displays at the end of the
        output of the simulation.
        """
        print('-'*50)
        print('Simulation is over. Total log of bikes is')
        pp(self.full_log)
        print('='*50)

    @property
    def full_log(self):
        """
        Returns
        -------
        The compiled log of all stations in this system.
        """
        full_log = []
        for station in self.stations:
            full_log.extend(station.log)
        return full_log

    def determine_destination(self, start_station_id):
        """
        Returns
        -------
        List index of random destination station.

        Parameters
        ----------
        start_station_id: [int] The list index of the station where the bike
        is checked out from.
        """
        station_ids = np.arange((len(self.stations)))
        station_ids = np.delete(station_ids, start_station_id)
        end_station_id = np.random.choice(station_ids)
        return end_station_id
    
    def determine_trip_duration(self, start_station_id, end_station_id):
        """
        Returns
        ---------
        The time the customer will take to ride the bike from the start location to the end location. Based on the manhattan distance between
        two locations.

        Parameters
        ----------
        start_station_id: [int] The list index of the station from which the 
        bike is checked out.

        end_station_id: [int] The list index of the station where the bike will
        check in.
        """
        loc_1 = self.stations[start_station_id].location
        loc_2 = self.stations[end_station_id].location
        distance = cityblock(loc_1, loc_2)
        time = distance / SPEED
        return int(time)

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

        # The test values are lower than the threshold, then True and a bike is 
        # checked out
        checkouts = checkout_thresholds >= test_values

        # Need to arr of booleans into the number of bikes that
        # will be attempted to check out this minute.
        stacked = np.stack([ks, checkouts], axis=-1)
        checkouts = [pair[0] if pair[1] else 0 for pair in stacked]
        
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
            
        # In the event that no stations are available
        return None
    
    def get_available_dock(self, station, availability):
        """
        Returns
        -------
        Randomly selected list index of a dock at the given station with one 
        available bike or one available dock. Random so as to not always pick 
        same docks from the list.

        Parameters
        ----------
        station: [Station] The station for which to check docks.

        availability: [str] Either 'check in' or 'check out'
        """
        num_docks = len(station.docks)
        random_indexes = np.arange(0, num_docks)
        np.random.shuffle(random_indexes)

        for i in random_indexes:
            if (availability == 'check out') and (station.docks[i].bike != None):
                return i
            elif (availability == 'check in') and (station.docks[i].bike == None):
                return i
            
        # In the event that no docks are available
        return None

# Calculate price and store in log.