from .dock import Dock

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

        size: [int > 0] number of docks that the station holds.
        """
        self.id = id
        self.location = location
        self.size = size
        self.init_docks()

    def init_docks(self):
        """
        Creates a list of Dock objects that can hold bikes. Docks do not move,
        and are the only part of the station that interacts with Bike objs.
        """
        self.docks = []
        for i in range(self.size):
            self.docks.append(Dock(i))

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
        for i in range(self.size):
            if self.docks[i].log:
                
                current_log = self.docks[i].log

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

    

