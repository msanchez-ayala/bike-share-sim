import copy
import pytest
from mock import Mock
import numpy as np
from sim.station import Station
from sim.dock import Dock
from sim.bike import ClassicBike
from sim.consts import CLASSIC_BASE_RATE

@pytest.fixture
def loc():
    return tuple(np.array([0, 0]))

def get_classic_bike():
    bike = Mock(spec = ClassicBike)
    return bike

def get_docks():
    dock_1 = Mock(spec = Dock)
    dock_1.log = []
    dock_1.bike = get_classic_bike()
    dock_2 = copy.deepcopy(dock_1)
    return dock_1, dock_2

@pytest.fixture
def station(loc):
    station = Station(0, loc, 2)
    station.docks[0], station.docks[1] = get_docks()
    return station


class TestStation: 

    def test_init_value_errors(self, loc):
        """
        Check that all appropriate value errors are thrown by __init__()
        """
        with pytest.raises(ValueError):
            loc_error = tuple(np.array([0, 0, 0]))

            Station(-1, loc, 1)      # id
            Station(0, loc_error, 1) # location
            Station(0, loc, -1)      # size

    def test_init_type_errors(self, loc):
        """
        Check that all appropriate type errors are thrown by __init__()
        """
        with pytest.raises(TypeError):
            loc_error_1 = (np.array([0.0, 0.0]))
            loc_error_2 = np.array([0, 0])

            Station(0.0, loc, 1)       # id
            Station(0, loc_error_1, 1) # location
            Station(0, loc_error_2, 1) # location
            Station(0, loc, '1')       # size

    def test_init_docks(self, loc):
        station = Station(1, loc, 4)
        assert len(station.docks) == 4\
            , "The incorrect number of docks was initialized"

        for i in range(station.size):
            assert station[i] == None, 'This dock space is not empty'
    
    def test_log(self, station):
        # Make sure empty log
        assert station.log == []\
            , "Log was wrongly instantiated with some activity"

        # Pretend a trip started and check log
        station.docks[0].log.append({
            'bike_id': 1,
            'trip_id': 1,
            'start_time': 10,
            'start_station_id': 1
        })
        assert station.log[0] == {
            'bike_id': 1,
            'trip_id': 1,
            'start_time': 10,
            'start_station_id': 0
        }, 'Not registering trips correctly (check out)'

        # Pretend a trip finished at another dock and check again
        station.docks[1].log.append({
            'bike_id': 2,
            'trip_id': 1,
            'end_time': 10,
            'end_station_id': 1
        })
        assert station.log[1] == {
            'bike_id': 2,
            'trip_id': 1,
            'end_time': 10,
            'end_station_id': 0
        }, 'Not registering trips correctly (check in)'
    
    def test_available_bikes(self, station):
        assert station.available_bikes == 2, 'Not registering number of bikes'

        station.docks[0].bike = None
        assert station.available_bikes == 1, 'Not registering change in bikes'
    
    def test_available_docks(self, station):
        assert station.available_docks == 0\
            , 'Not registering correct no. of docks'

        station.docks[1].bike = None
        assert station.available_docks == 1, "Not registering change in bikes"

        station.docks[0].bike = None
        assert station.available_docks == 2, "Not registering change in bikes"
    
    def test__getitem__(self, station):
        assert isinstance(station[0], Dock)\
            , 'Not able to index. Check constructor'
        with pytest.raises(IndexError):
            station[2]
    
    def test__iter__(self, station):
        for dock in station:
            assert isinstance(dock, Dock), 'Not able to loop. Check constructor'
    