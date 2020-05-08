import unittest
from sim.bike import Bike, ClassicBike, ElectricBike

class TestBike(unittest.TestCase):

    print('testing Bike')

    def setUp(self):
        print('Setting up')
        self.bike = Bike(1)

    def tearDown(self):
        print('Tearing down\n')

    def test_ride(self):

        self.assertEqual(self.bike._uses, 0)
        self.assertEqual(self.bike.condition, 'good')
        
        for _ in range(50):
            self.bike.ride()
        
        self.assertEqual(self.bike._uses, 50)
        self.assertEqual(self.bike.condition, 'fair')

        for _ in range(50):
            self.bike.ride()

        self.assertEqual(self.bike._uses, 100)
        self.assertEqual(self.bike.condition, 'poor')

        for _ in range(50):
            self.bike.ride()
        
        self.assertEqual(self.bike._uses, 150)
        self.assertEqual(self.bike.condition, 'no service')
        

class TestClassicBike(unittest.TestCase):

    print('testing ClassicBike')

    def setUp(self):
        print('Setting up')
        self.bike = ClassicBike(1)

    def tearDown(self):
        print('Tearing down\n')
    
    def test_price(self):
        self.assertEqual(self.bike.price(45), 5.00)
        self.assertEqual(self.bike.price(10), 3.50)
        self.assertEqual(self.bike.price(30), 3.50)


class TestElectricBike(unittest.TestCase):

    print('testing ElectricBike')

    def setUp(self):
        print('Setting up')
        self.bike = ElectricBike(1)

    def tearDown(self):
        print('Tearing down\n')

    def test_price_cases(self):
        self.assertEqual(self.bike.price(45), 8.25)
        self.assertEqual(self.bike.price(10), 5.25)
        self.assertEqual(self.bike.price(30), 5.25)

    # def test_update_charge(self):
    #     pass


if __name__ == '__main__':
    unittest.main()