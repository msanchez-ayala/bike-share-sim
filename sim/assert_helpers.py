"""
A module of assert helpers for the models in this project.
"""

def assert_greater_than_zero(var, name):
    """
    Raises ValueError if value is less than zero.

    Parameters
    ----------
    var: [int or float] Any number that must be greater than or equal to zero.

    name: [str] The name of the variable to put into the error message.
    """
    if var < 0:
        raise ValueError(f'{name} must be greater than or equal to zero')

def assert_id(id):
    if not isinstance(id, int):
        raise TypeError('id must be an int')
    else:
        assert_greater_than_zero(id, 'id')
    
