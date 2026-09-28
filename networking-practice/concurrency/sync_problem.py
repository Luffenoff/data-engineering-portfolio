import time
import asyncio



async def slow_task(name, delay):
    print(f"[{name}] Начал работу")
    await asyncio.sleep(delay) # симуляция ожидания ответа
    print(f"[{name}] Закончил за {delay} сек")
 
 
async def main():   
    start = time.time()

    await asyncio.gather(
        slow_task("Задача 1", 2),
        slow_task("Задача 2", 2),
        slow_task("Задача 3", 2),
    )

    print(f"Всего заняло {time.time() - start:.2f} сек")
    
    
asyncio.run(main())