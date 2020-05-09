from .consts import *

class Bike:
    """
    Base class for Bikes. 
    
    DO NOT instantiate this class directly, but rather one of the subclasses defined below here: ClassicBike or ElectricBike. Some methods 
    (e.g. price()) will only work for subclasses of Bike.
    """

    conditions = CONDITIONS

    def __init__(self, id):
        """
        Parameters
        ----------
        id: [int >= 0] the id no. for the bike.

        rate: [float >= 0] the cost per 30-minute ride.
        """
        self.id = id
        self.condition = self.conditions[0]
        self._uses = 0

        # Overridden by subclasses
        self.base_rate = None
        self.add_rate = None
    
    def update_condition(self):
        """
        Every 50 rides the condition is updated.
        """
        if self._uses == 50:
            # fair
            self.condition = self.conditions[1]
        
        elif self._uses == 100:
            # poor
            self.condition = self.conditions[2]
        
        elif self._uses == 150:
            self.condition = self.conditions[3]

    def ride(self):
        """
        Triggers a bike ride. Every ride is logged and the condition of the 
        bike is updated.

        If bike is out of service, try another dock.
        """
        # Update when ready to consider wear/tear
        self._uses += 1
        self.update_condition()

        # # If condition isn't 'no service'
        # if self.condition != self.conditions[3]:
        #     self._uses += 1
        #     self.update_condition()
        
        # # Don't let people ride a bike that is in poor condition
        # else:
        #     return 'Bike out of service'
    
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
        Bike.__init__(self, id)
        self.base_rate = CLASSIC_BASE_RATE
        self.add_rate = CLASSIC_ADD_RATE


class ElectricBike(Bike):
    """
    Subclass for the electric bike option which introduces battery 
    consideration.
    """

    def __init__(self, id):
        Bike.__init__(self, id)
        self.base_rate = ELECTRIC_BASE_RATE
        self.add_rate = ELECTRIC_ADD_RATE
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