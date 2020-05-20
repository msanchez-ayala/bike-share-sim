import unittest
import numpy as np
from sim.station import Station
from sim.dock import Dock
from sim.bike import ClassicBike
from sim.consts import CLASSIC_BASE_RATE

class TestStation(unittest.TestCase):
    def setUp(self):
        """
        Only recurring thing is the location with numpy.int values.
        """
        self.loc = tuple(np.array([0, 0]))
        

    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            loc_error = tuple(np.array([0, 0, 0]))

            self.station = Station(-1, self.loc, 1)     # id
            self.station = Station(0, loc_error, 1)  # location
            self.station = Station(0, self.loc, -1)    # size
            self.station = Station(0, self.loc, 0)     # docks
            self.station = Station(0, self.loc, 21)     # docks
            self.station = Station(0, self.loc, 2, 3)  # num_bikes
            self.station = Station(0, self.loc, 2, -1) # num_bikes
        
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with self.assertRaises(TypeError):
            loc_error_1 = (np.array([0.0, 0.0]))
            loc_error_2 = np.array([0, 0])

            self.station = Station(0.0, self.loc, 1)     # id
            self.station = Station(0, loc_error_1, 1)      # location
            self.station = Station(0, loc_error_2, 1)    # location
            self.station = Station(0, self.loc, '1')    # size
            self.station = Station(0, self.loc, 2, '1') # num_bikes

    def test_init_docks_empty(self):
        """
        Test where all docks are empty.
        """
        self.station = Station(1, self.loc, 4)
        for i in range(self.station.size):
            self.assertIsInstance(self.station.docks[i], Dock)
    
    def test_init_docks_filled(self):
        """
        Test where some docks are empty and some are filled.
        """
        self.station = Station(1, self.loc, 3, 2, 0)

        # Assert number of bikes is appropriate and have correct IDs
        self.assertEqual(self.station.docks[0].bike.id, 0)
        self.assertEqual(self.station.docks[1].bike.id, 1)
        self.assertIsNone(self.station.docks[2].bike)        
    
    def test_log(self):
        self.station = Station(1, self.loc, 4)

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
        self.station.docks[2].check_in(bike_2, 15, 15)
        self.assertEqual(self.station.log[1], {
            'bike_id': 2,
            'trip_id': 0, # Fix this if we fix dock code
            'end_time': 15,
            'end_station_id': 1,
            'price': CLASSIC_BASE_RATE,
            'duration': 15
        })
    
    def test_available_bikes(self):
        self.station = Station(0, self.loc, 3, 2, 0)
        self.assertEqual(self.station.available_bikes, 2)

        self.station.docks[0].check_out(0)
        self.assertEqual(self.station.available_bikes, 1)

        self.station = Station(0, self.loc, 1)
        self.assertEqual(self.station.available_bikes, 0)
    
    def test_available_docks(self):
        self.station = Station(0, self.loc, 3, 2, 0)
        self.assertEqual(self.station.available_docks, 1)

        self.station.docks[0].check_out(0)
        self.assertEqual(self.station.available_docks, 2)

        self.station = Station(0, self.loc, 1, 1, 0)
        self.assertEqual(self.station.available_docks, 0)
    
    def test__getitem__(self):
        self.station = Station(0, self.loc, 3, 1, 0)

        self.assertIsInstance(self.station[0], Dock)
        self.assertEqual(self.station[0].bike.id, 0)
        self.assertIsNone(self.station[1].bike)

        with self.assertRaises(IndexError):
            self.station[3]
    
    def test__iter__(self):
        self.station = Station(0, self.loc, 3, 1, 0)

        for dock in self.station:
            self.assertIsInstance(dock, Dock)
    

if __name__ == '__main__':
    unittest.main()