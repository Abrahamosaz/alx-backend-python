#!/usr/bin/env python3
import asyncio
import random
from typing import Generator
"""
write a async python generator
"""


async def async_generator() -> Generator[float, None, None]:
    """
    generator that yet random  value between 0, 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
