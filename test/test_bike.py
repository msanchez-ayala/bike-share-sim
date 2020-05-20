import unittest
from sim.bike import Bike, ClassicBike, ElectricBike

class TestBike(unittest.TestCase):

    print('testing Bike')

    def setUp(self):
        self.bike = Bike(1)
    
    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            self.bike = Bike(-1)        # id
    
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with self.assertRaises(TypeError):
            self.bike = Bike('A')        # id

    def test_ride(self):

        self.assertEqual(self.bike.trip_id, 0)
        
        for _ in range(50):
            self.bike.ride()
        
        self.assertEqual(self.bike.trip_id, 50)

        for _ in range(50):
            self.bike.ride()

        self.assertEqual(self.bike.trip_id, 100)

        for _ in range(50):
            self.bike.ride()
        
        self.assertEqual(self.bike.trip_id, 150)
    

class TestClassicBike(unittest.TestCase):

    print('testing ClassicBike')

    def setUp(self):
        self.bike = ClassicBike(1)
    
    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with self.assertRaises(ValueError):
            self.bike = ClassicBike(-1) # id
    
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with self.assertRaises(TypeError):
            self.bike = ClassicBike('A') # id
    
    def test_price(self):
        self.assertEqual(self.bike.price(45), 5.00)
        self.assertEqual(self.bike.price(10), 3.50)
        self.assertEqual(self.bike.price(30), 3.50)


class TestElectricBike(unittest.TestCase):

    pass


if __name__ == '__main__':
    unittest.main()