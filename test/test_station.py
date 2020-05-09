import unittest
from sim.station import Station
from sim.dock import Dock
from sim.bike import ClassicBike

class TestStation(unittest.TestCase):

    # def setUp(self):
    #     self.station_1 = Station(1, (0, 0), 4)
    #     self.station_2 = Station(2, (3, 3), 8)
    
    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            self.station = Station(-1, (0,0), 1)     # id
            self.station = Station(0, (0, 0, 0), 1)  # location
            self.station = Station(0, (0, 0), -1)    # size
            self.station = Station(0, (0, 0), 2, 3)  # num_bikes
            self.station = Station(0, (0, 0), 2, -1) # num_bikes
        
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with self.assertRaises(TypeError):
            self.station = Station(0.0, (0,0), 1)     # id
            self.station = Station(0, [0, 0], 1)      # location
            self.station = Station(0, (0, '0'), 1)    # location
            self.station = Station(0, (0, 0), '1')    # size
            self.station = Station(0, (0, 0), 2, '1') # num_bikes

    def test_init_docks_empty(self):
        """
        Test where all docks are empty.
        """
        self.station = Station(1, (0, 0), 4)
        for i in range(self.station.size):
            self.assertIsInstance(self.station.docks[i], Dock)
    
    def test_init_docks_filled(self):
        """
        Test where some docks are empty and some are filled.
        """
        self.station = Station(1, (0,0), 3, 2, 0)

        # Assert number of bikes is appropriate and have correct IDs
        self.assertEqual(self.station.docks[0].bike.id, 0)
        self.assertEqual(self.station.docks[1].bike.id, 1)
        self.assertIsNone(self.station.docks[2].bike)        
    
    def test_log(self):
        self.station = Station(1, (0, 0), 4)

        # Empty log
        self.assertEqual(self.station.log, [])

        # Instatiate some bikes and populate 
        bike_1 = ClassicBike(1)
        bike_2 = ClassicBike(2)

        self.station.docks[0].bike = bike_1
        self.station.docks[1].bike = bike_2

        # Make a bike move and check log again
        self.station.docks[0].check_out(10, self.station) # station_1 redundant
        self.assertEqual(self.station.log, [{
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'start_time': 10,
            'start_station_id': 1 # Fix this if we fix dock code
        }])

        # Make a bike move at a different station and check log again

if __name__ == '__main__':
    unittest.main()