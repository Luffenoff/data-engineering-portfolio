import time


def slow_task(name, delay):
    print(f"[{name}] Начал работу")
    time.sleep(delay) # симуляция ожидания ответа
    print(f"[{name}] Закончил за {delay} сек")
    
start = time.time()

slow_task("Задача 1", 2)
slow_task("Задача 2", 2)
slow_task("Задача 3", 2)


print(f"Всего заняло {time.time() - start:.2f} сек")