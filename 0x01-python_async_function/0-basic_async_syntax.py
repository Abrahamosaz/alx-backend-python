#!/usr/bin/env python3
import asyncio
import random
"""
async coroutine function that take integer value
and wait for a random delay between o and the int arg
"""


async def wait_random(max_delay: float = 10) -> float:
    """
    wait for random seconds
    """
    random_num = random.random() * max_delay
    await asyncio.sleep(random_num)
    return random_num
