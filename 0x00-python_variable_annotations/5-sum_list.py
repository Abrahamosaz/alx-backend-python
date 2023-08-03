#!/usr/bin/env python3
from functools import reduce
from typing import List
"""
function that take a list of float and return
their sum as a float
"""


def sum_list(input_list: List[float]) -> float:
    """
    Take a list of float and return the
    sum of the float
    """
    return reduce(lambda a, b: a + b, input_list)
