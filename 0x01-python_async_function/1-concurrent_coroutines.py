#!/usr/bin/env python3
"""a module that execute coroutines at the same time"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax.py').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """returns the list of all the delays (float values)"""
    delays = await asyncio.gather(
        *tuple(map(lambda _: wait_random(max_delay), range(n)))
    )
    return sorted(delays)
