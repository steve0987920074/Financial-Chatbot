"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""

from functions import *
import math

def test_end_chat():
    assert end_chat("bye") == True
    assert end_chat("quit") == True
    assert end_chat("blarch") != True
    assert end_chat("BYE") != True
    assert isinstance(end_chat("bye"), bool)
    
def test_calc_parameter():
    assert math.isclose(calc_parameter({'input_string': 'present value', 'future value': 50000.0, 'payment': 500.0, 'required rate per year': 0.05, 'required time period': 5.0},"present value"), 37012, rel_tol = 1)
    assert calc_parameter({'input_string': 'present value', 'future value': 1, 'payment': 2, 'required rate per year': 3, 'required time period': 4},"present value") != None
    assert calc_parameter({'input_string': 'present value', 'future value': 3, 'payment': 0.4, 'required rate per year': 0.05, 'required time period': 5.0},"present value") not in unknown_input_reply
    assert calc_parameter({'input_string': 'present value'},"present value") == None
    assert calc_parameter({'input_string': 'value', 'future value': 3, 'payment': 0.4, 'required rate per year': 0.05, 'required time period': 5.0},"value") in unknown_input_reply
    assert isinstance(calc_parameter({'input_string': 'present value', 'future value': 5, 'payment': 5, 'required rate per year': 5, 'required time period': 5.},"present value"), float)    