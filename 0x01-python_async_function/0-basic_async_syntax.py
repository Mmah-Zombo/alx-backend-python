#!/usr/bin/env python3
"""a module that holds a synchronous coroutine"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """an asynchronous coroutine"""
    value = random.uniform(0, max_delay)
    await asyncio.sleep(value)
    return value
