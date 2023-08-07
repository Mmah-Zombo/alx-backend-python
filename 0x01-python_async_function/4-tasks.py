#!/usr/bin/env python3
"""more async code"""
import asyncio
from typing import List
from random import uniform


task_wait_random = __import__('3-tasks').task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """a function that is similar to wait_n"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
