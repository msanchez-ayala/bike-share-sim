import pytest
from sim.bike import Bike, ClassicBike

class TestBike:

    print('testing Bike')

    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with pytest.raises(ValueError):
            Bike(-1)       
    
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with pytest.raises(TypeError):
            Bike('A')      
            Bike(True)  
            Bike([0])    

    def test_ride(self):
        bike = Bike(0)
        message_init = 'trip_id not initializing correctly'
        message_add = 'trip_id attribute not adding rides correctly'

        assert bike.trip_id == 0, message_init
        
        for _ in range(50):
            bike.ride()
        
        assert bike.trip_id == 50, message_add
    

class TestClassicBike:

    def setup_method(self, method):
        self.classic_bike = ClassicBike(0)
    
    def teardown_method(self, method):
        self.classic_bike = None
    
    def test_price(self):
        message = 'ClassicBike pricing is not working correctly'

        assert self.classic_bike.price(45) == 5.00, message
        assert self.classic_bike.price(10) == 3.50, message
        assert self.classic_bike.price(30) == 3.50, message
        assert self.classic_bike.price(0) == 3.50, message
    
    def test_price_error(self):
        with pytest.raises(ValueError):
            self.classic_bike.price(-1)
            self.classic_bike.price(-30)
            self.classic_bike.price(-45)