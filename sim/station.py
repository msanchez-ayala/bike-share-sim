from .dock import Dock

class Station:
    """
    Stations hold docks and store a log of bike entries and exits.
    """

    def __init__(self, id, location, size):
        """
        Creates a new Station.

        Parameters
        ----------
        id: [int] the id no. for the station.
        location: [tuple] coordinates of the station.
        size: [int] number of docks that the station holds.
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
            # self.docks.append(Dock(ARGS))
            pass

    @property
    def log(self):
        """
        Returns
        --------
        Full log of activities from all docks in this station.
        """
        log = []

        # Go through each dock and access the log attribute. Append to full log
        # and return
        for i in range(size):
            if self.docks[i]:
                log.append(docks)

    

