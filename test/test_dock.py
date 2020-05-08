import unittest
from sim.dock import Dock
from sim.bike import ClassicBike
from sim.station import Station

class TestDock(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.dock = Dock(1)
        
        # Instantiate a bike and station. Ride bike into this dock
        self.bike = ClassicBike(1)
        self.station = Station(1, (0, 0), 1)
        self.bike.ride()

    def tearDown(self):
        print('tearDown\n')
    
    def test_check_in(self):
        self.assertIsNone(self.dock.bike)
        
        # Check bike in 5 mins after init at station
        self.dock.check_in(self.bike, 5, self.station)

        self.assertIsInstance(self.bike, ClassicBike)
        self.assertEqual(self.bike.id, 1)
        self.assertEqual(self.dock.log[0], {
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'end_time': 5,
            'end_station_id': 1, # same as above
        })

    def test_check_out(self):

        # Check bike in 5 mins after init at station
        self.dock.check_in(self.bike, 5, self.station)
        self.dock.check_out(10, self.station)

        self.assertIsNone(self.dock.bike)
        self.assertEqual(self.dock.log[1], {
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'start_time': 10,
            'start_station_id': 1 # Same as above
        })








if __name__ == '__main__':
    unittest.main()