import threading
import time


def cpu_bound_task(n):
    """Чисто вычислительная задача - считаем сумму квадратов"""
    total = 0
    for i in range(n):
        total += i * i
    return total


