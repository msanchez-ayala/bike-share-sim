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
    
@pytest.fixture
def classic_bike():
    yield ClassicBike(0)

class TestClassicBike:
    
    def test_price(self, classic_bike):
        message = 'ClassicBike pricing is not working correctly'

        assert classic_bike.price(45) == 5.00, message
        assert classic_bike.price(10) == 3.50, message
        assert classic_bike.price(30) == 3.50, message
        assert classic_bike.price(0) == 3.50, message
    
    def test_price_error(self, classic_bike):
        with pytest.raises(ValueError):
            classic_bike.price(-1)
            classic_bike.price(-30)
            classic_bike.price(-45)