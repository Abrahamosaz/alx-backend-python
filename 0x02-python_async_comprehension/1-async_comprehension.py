#!/usr/bin/env python
import asyncio
import random
from typing import List
"""
async_comprehension function
"""

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """
    retrieve value from the async_generator
    """
    return [num async for num in async_generator()]
