from .consts import *
from .assert_helpers import assert_id, assert_greater_than_zero

class Bike:
    """
    Base class for Bikes. 
    
    DO NOT instantiate this class directly, but rather one of the subclasses defined below here: ClassicBike or ElectricBike. Some methods 
    (e.g. price()) will only work for subclasses of Bike.
    """

    def __init__(self, id):
        """
        Parameters
        ----------
        id: [int >= 0] the id no. for the bike.

        rate: [float >= 0] the cost per 30-minute ride.
        """
        assert_id(id)

        self._id = id
        self._trip_id = 0

        # Overridden by subclasses
        self._base_rate = None
        self._add_rate = None

    @property
    def id(self):
        return self._id

    @property
    def trip_id(self):
        return self._trip_id

    def ride(self):
        """
        Triggers a bike ride. Every ride is logged and the condition of the 
        bike is updated (later when want to implement this). If bike is out of service, try another dock.
        """
        # Update when ready to consider wear/tear
        self._trip_id += 1
    
    def price(self, duration):
        """
        Calculates the amount a rider owes. Does not work in the base Bike 
        class because no defined base or additional rates. Should always be 
        called after ride.

        Returns
        -------
        price: The total a rider owes for their ride.

        Parameters
        ----------
        duration: [int >= 0] How many minutes the ride was.
        """
        assert_greater_than_zero(duration, 'duration')
        
        if duration > 30:
            price = self.base_rate + (duration - 30) * self.add_rate
            return price
        
        else:
            return self.base_rate

class ClassicBike(Bike):
    """
    Subclass for the classic bike option.
    """
    def __init__(self, id):
        super().__init__(id)
        self._base_rate = CLASSIC_BASE_RATE
        self._add_rate = CLASSIC_ADD_RATE

    @property
    def base_rate(self):
        return self._base_rate

    @property
    def add_rate(self):
        return self._add_rate

class ElectricBike(Bike):
    """
    Subclass for the electric bike option which introduces battery 
    consideration.
    """

    def __init__(self, id):
        super().__init__(id)
        self._base_rate = ELECTRIC_BASE_RATE
        self._add_rate = ELECTRIC_ADD_RATE
        self.charge = ELECTRIC_MAX_CHARGE
    
    def update_charge(self):
        """
        Figure out how to deal with this. One possibility:

        - Start at 100
        - Each minute drains 2 charge
        - Each minute in a station recharges 5 charge
        - Motor stops working if charge reaches 0
        - Can only check one out if charge is above 60 (enough for 30-min ride)
        """
        pass


