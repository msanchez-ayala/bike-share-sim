from .consts import CONDITIONS
from .assert_helpers import assert_id
from .bike import Bike, ClassicBike

class Dock:
    """
    A Dock to hold bikes. Each dock resides in 
    """
    conditions = CONDITIONS

    def __init__(self, id, bike = None):
        """
        Parameters
        ----------
        id: [int >= 0] the id no. for the station.

        bike: [Bike | None] The Bike or None value to occupy this dock.
        """
        assert_id(id)

        self.__id = id
        self.bike = bike
        self.__log = []
    
    @property
    def id(self):
        return self.__id
    
    @property
    def bike(self):
        return self.__bike
    
    @bike.setter
    def bike(self, bike):
        if (bike == None) or (isinstance(bike, Bike)):
            self.__bike = bike
        else:
            raise TypeError('bike must be a Bike object or None')
    
    @property
    def log(self):
        return self.__log
    
    def check_in(self, bike, time, duration):
        """
        Check a bike into this dock.

        Parameters
        ----------
        bike: [Bike] The bike parking at this station.

        time: [int] The time at which the bike is checked in.

        duration: [int] The number of minutes this trip lasted
        """
        self.bike = bike
        price = self.bike.price(duration)

        self.__log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike.trip_id,
            'end_time': time,
            'price': price,
            'duration': duration
        })

    def check_out(self, time):
        """
        Check a bike out of this dock.

        Parameters
        ----------
        time: [int] The time at which the bike is checked out.
        """
        self.bike.ride()

        self.__log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike.trip_id,
            'start_time': time
        })
        
        # Store bike to return before clearing self.bike
        bike = self.bike
        self.bike = None
        return bike


