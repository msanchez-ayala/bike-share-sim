from station import Station

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
            Station(0, (0, 0), 1, 1, 1),
            Station(1, (1, 1), 1, 0, 2)
        ]

        self.run(60)
    
    def run(self, length):
        """
        Runs the simulation.
        """
        # for minute in range(length):
        #     pass
        print(self.stations)
