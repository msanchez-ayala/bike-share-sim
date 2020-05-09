import unittest
from sim.station import Station
from sim.dock import Dock
from sim.bike import ClassicBike

class TestStation(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.station_1 = Station(1, (0, 0), 4)
        self.station_2 = Station(2, (3, 3), 8)



    def tearDown(self):
        print('tearDown\n')

    def test_init_docks(self):
        for i in range(self.station_1.size):
            self.assertIsInstance(self.station_1.docks[i], Dock)
    
    def test_log(self):
        # Empty log
        self.assertEqual(self.station_1.log, [])

        # Instatiate some bikes and populate 
        bike_1 = ClassicBike(1)
        bike_2 = ClassicBike(2)

        self.station_1.docks[0].bike = bike_1
        self.station_1.docks[1].bike = bike_2

        # Make a bike move and check log again
        self.station_1.docks[0].check_out(10, self.station_1) # station_1 redundant
        self.assertEqual(self.station_1.log, [{
            'bike_id': 1,
            'trip_id': 1, # Fix this if we fix dock code
            'start_time': 10,
            'start_station_id': 1 # Fix this if we fix dock code
        }])

        # Make a bike move at a different station and check log again

if __name__ == '__main__':
    unittest.main()