import unittest
from sim.station import Station
from sim.dock import Dock
from sim.bike import ClassicBike

class TestStation(unittest.TestCase):
    
    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            self.station = Station(-1, (0,0), 1)     # id
            self.station = Station(0, (0, 0, 0), 1)  # location
            self.station = Station(0, (0, 0), -1)    # size
            self.station = Station(0, (0, 0), 0)     # docks
            self.station = Station(0, (0, 0), 21)     # docks
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

        # Make a bike move and check log again
        self.station.docks[0].check_out(10)
        self.assertEqual(self.station.log[0], {
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'start_time': 10,
            'start_station_id': 1
        })

        # Make a different bike move at another dock and check again
        self.station.docks[2].check_in(bike_2, 15)
        self.assertEqual(self.station.log[1], {
            'bike_id': 2,
            'trip_id': 0, # Fix this if we fix dock code
            'end_time': 15,
            'end_station_id': 1
        })
    
    def test_available_bikes(self):
        self.station = Station(0, (0, 0), 3, 2, 0)
        self.assertEqual(self.station.available_bikes, 2)

        self.station.docks[0].check_out(0)
        self.assertEqual(self.station.available_bikes, 1)

        self.station = Station(0, (0, 0), 1)
        self.assertEqual(self.station.available_bikes, 0)
    
    def test_available_docks(self):
        self.station = Station(0, (0, 0), 3, 2, 0)
        self.assertEqual(self.station.available_docks, 1)

        self.station.docks[0].check_out(0)
        self.assertEqual(self.station.available_docks, 2)

        self.station = Station(0, (0, 0), 1, 1, 0)
        self.assertEqual(self.station.available_docks, 0)

if __name__ == '__main__':
    unittest.main()