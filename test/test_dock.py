import unittest
from sim.dock import Dock
from sim.bike import ClassicBike
from sim.station import Station
from sim.consts import CLASSIC_BASE_RATE

class TestDock(unittest.TestCase):

    def setUp(self):
        self.dock = Dock(1)
        
        # Instantiate a bike and station. Ride bike into this dock
        self.bike = ClassicBike(1)
        self.station = Station(1, (0, 0), 1)
        self.bike.ride()

    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            self.dock = Dock(-1)
    
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with self.assertRaises(TypeError):
            self.dock = Dock('A')             # id
            self.dock = Dock(1, 'Not a Bike') # ClassicBike instance
    
    def test_check_in(self):
        self.assertIsNone(self.dock.bike)
        
        # Check bike in 5 mins after init at station
        self.dock.check_in(self.bike, 5, 5)

        self.assertIsInstance(self.bike, ClassicBike)
        self.assertEqual(self.bike.id, 1)
        self.assertEqual(self.dock.log[0], {
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'end_time': 5,
            'price': CLASSIC_BASE_RATE,
            'duration': 5
        })

    def test_check_out(self):

        # Check bike in 5 mins after init at station (since the dock was 
        # initialized without a bike in it

        self.dock.check_in(self.bike, 5, 5)
        
        self.dock.check_out(10)

        self.assertIsNone(self.dock.bike)
        self.assertEqual(self.dock.log[1], {
            'bike_id': 1,
            'trip_id': 2, # 2 because setUp() and checkout() both invoke ride()
            'start_time': 10
        })


if __name__ == '__main__':
    unittest.main()