#!/usr/bin/env python3
"""Async Generator"""
import asyncio
import random


async def async_generator():
    """loops 10 times, then yield a random number between 0 & 10"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
