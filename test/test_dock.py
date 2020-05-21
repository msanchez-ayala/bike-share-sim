import pytest
from mock import Mock
import numpy as np
from sim.dock import Dock
from sim.bike import ClassicBike
from sim.consts import CLASSIC_BASE_RATE

@pytest.fixture
def dock():
    return Dock(0)

@pytest.fixture
def classic_bike():
    mocked_bike = Mock(spec = ClassicBike)
    mocked_bike.id = 0
    mocked_bike.trip_id = 0
    mocked_bike.price.return_value = CLASSIC_BASE_RATE
    return mocked_bike

class TestDock:

    def test_init_value_errors(self):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with pytest.raises(ValueError):
            Dock(-1)
    
    def test_init_type_errors(self):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with pytest.raises(TypeError):
            Dock('A')             # id
            Dock(True)            # id
            Dock(0, 'Not a Bike') # bike arg
    
    def test_check_in(self, dock, classic_bike):
     
        assert dock.bike is None, 'Dock was wrongly instantiated with a bike.'
        
        # Check bike in 5 mins after init at station
        dock.check_in(classic_bike, 5, 5)

        assert dock.log[0] == {
            'bike_id': 0,
            'trip_id': 0,
            'end_time': 5,
            'price': CLASSIC_BASE_RATE,
            'duration': 5
        }

    def test_check_out(self, dock, classic_bike):

        # Check bike in 5 mins after init at station (since the dock was 
        # initialized without a bike in it

        dock.check_in(classic_bike, 5, 5)

        # Add 1 to bike's trip id as check_out() normally would. Must go before
        # check_out() call because the new trip_id is part of the return stmt.
        classic_bike.trip_id += 1

        dock.check_out(10)

        assert dock.bike == None
        assert dock.log[1] == {
            'bike_id': 0,
            'trip_id': 1,
            'start_time': 10
        }