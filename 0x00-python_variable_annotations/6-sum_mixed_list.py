#!/usr/bin/python
from typing import List, Union
"""
function that take both integer and float
and return the sum in float
"""


def sum_mixed_list(mxd_lst: List(Union(int, float))) -> float:
    """
    take and list of both int and float and sum the result
    as a float
    """
    return sum(mxd_lst)
