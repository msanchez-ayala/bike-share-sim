from .consts import CONDITIONS

class Dock:
    """
    A Dock to hold bikes. Each dock resides in 
    """
    conditions = CONDITIONS

    def __init__(self, id):
        self.id = id
        self.bike = None
        self.condition = self.conditions[0]
        self.log = []
    
    def check_in(self, bike, time, station):
        """
        Check a bike into this dock.

        Parameters
        ----------
        bike: [Bike] The bike parking at this station.

        time: [int] The time in minutes since the simulation began.

        station: [int] The station id corresponding to where this dock resides.
        """
        self.bike = bike
        self.log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike._uses, # This line may mess us up. not sure how to track yet
            'end_time': time,
            'end_station_id': station.id, # This line may also mess us up
        })

    def check_out(self, time, station):
        """
        Check a bike out of this dock.

        Parameters
        ----------
        time: [int] The time in minutes since the simulation began.

        station: [int] The station id corresponding to where this dock resides.
        """
        self.log.append({
            'bike_id': self.bike.id,
            'trip_id': self.bike._uses, # This line may mess us up. not sure how to track yet
            'start_time': time,
            'start_station_id': station.id # This line may also mess us up
        })

        self.bike = None
    

