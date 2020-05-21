from .dock import Dock
from .bike import ClassicBike
from .assert_helpers import assert_greater_than_zero
import numpy as np

class Station:
    """
    Stations hold multiple docks and can retrieve a compiled log of bike 
    entries and exits.
    """

    def __init__(self, id, location, size):
        """
        Creates a new Station.

        Parameters
        ----------
        id: [int >= 0] the id no. for the station.

        location: [tuple] coordinates of the station.

        size: [1 <= int <= 20] number of docks that the station holds.

        num_bikes: [0 < int < self.size] (optional) The number of bikes to put 
                   into this station. Should only be omitted if we want all docks to be empty.
        
        bike_id_start: [0 <= int <= num_bikes] (Optional) The id with which to  
                       start numbering bikes.
        """
        # Assert all inputs
        self.assert_id(id)
        self.assert_location(location)
        self.assert_size(size)

        self.id = id
        self.location = location
        self.size = size
        self.docks = self.init_docks()

    def init_docks(self):
        """
        Creates an empty list for Dock objects that can hold bikes. Docks do not move, and are the part of the station that interacts with Bikes.
        """
        return [None] * self.size

    @property
    def log(self):
        """
        Returns
        --------
        Full log of activities from all docks in this station.
        """
        result = []

        # Go through each dock and access the log attribute. Append to full log
        # and return
        for dock in self.docks:
            if dock.log:
                current_log = dock.log
                for trip in current_log:

                    # If this is start of a trip, add start station
                    if trip.get('start_time'):
                        trip['start_station_id'] = self.id

                    # If it's an end of a trip, add end station
                    elif trip.get('end_time'):
                        trip['end_station_id'] = self.id

                    # Add all individual trips to the total log
                    result.append(trip)

        return result
    
    @property
    def available_bikes(self):
        """
        Returns
        -------
        The number of bikes currently docked at this station.
        """
        bikes = 0

        for dock in self.docks:
            if dock.bike:
                bikes += 1
        
        return bikes
    
    @property
    def available_docks(self):
        return self.size - self.available_bikes
    
    def __getitem__(self, key):
        self.assert_index(key)
        return self.docks[key]

    def __iter__(self):
        return iter(self.docks)

    ### ASSERT HELPERS ###

    def assert_id(self, id):
        if not isinstance(id, int):
            raise TypeError('id must be an int')
        
        assert_greater_than_zero(id, 'id')
    
    def assert_location(self, location):
        if not isinstance(location, tuple):
            raise TypeError('location must be a tuple with coordinates')
            
        if len(location) != 2:
            raise ValueError('location must contain only 2 elements')
        
        for coord in location:
            if not isinstance(coord, np.int64):
                raise TypeError('coordinates must be np.int64')
        
    def assert_size(self, size):
        if not isinstance(size, int):
            raise TypeError('size must be an int')

        if (size < 1 ) or (size > 20) :
            raise ValueError('size must be in [1, 20].')

    def assert_index(self, key):
        if key > self.size - 1:
            raise IndexError('There do not exist this many docks')