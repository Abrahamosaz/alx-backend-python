#!/usr/bin/env python3
from typing import List
"""
async_comprehension function
"""

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """
    retrieve value from the async_generator and return a list of values
    """
    return [num async for num in async_generator()]
