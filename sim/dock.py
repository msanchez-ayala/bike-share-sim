from .consts import CONDITIONS
from .assert_helpers import assert_id
from .bike import ClassicBike

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
        self.assert_bike(bike)

        self.id = id
        self.bike = bike
        self.condition = self.conditions[0]
        self.log = []
    
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

        self.log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike._uses, # This line may mess us up. not sure how to track yet
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

        self.log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike._uses, # This line may mess us up. not sure how to track yet
            'start_time': time
        })
        
        # Store bike to return before clearing self.bike
        bike = self.bike
        self.bike = None
        return bike
    

    ### ASSERTION HELPERS ### 
    

    def assert_bike(self, bike):
        if bike:
            if not isinstance(bike, ClassicBike):
                raise TypeError('This bike is not a ClassicBike')

