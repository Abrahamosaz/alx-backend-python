#!/usr/bin/env python3
import asyncio
import time
"""
function excute async in parallel using asyncio.gather
"""

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    excute function in parallel using asyncio.gather function 
    """
    start_time = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    return time.time() - start_time
