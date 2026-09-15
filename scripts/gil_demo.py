import threading
import time
import multiprocessing


def cpu_bound_task(n):
    """Чисто вычислительная задача - считаем сумму квадратов"""
    total = 0
    for i in range(n):
        total += i * i
    return total


N = 50_000_000


if __name__ == "__main__":
    start = time.time()
    cpu_bound_task(N)
    cpu_bound_task(N)
    print(f"Последовательно (2 задачи): {time.time() - start:.2f} сек")


    start = time.time()
    t1 = threading.Thread(target=cpu_bound_task, args=(N,))
    t2 = threading.Thread(target=cpu_bound_task, args=(N,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"В двух потоках: {time.time() - start:.2f} сек")
    
    start = time.time()
    p1 = multiprocessing.Process(target=cpu_bound_task, args=(N,))
    p2 = multiprocessing.Process(target=cpu_bound_task, args=(N,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(f"В двух процессах: {time.time() - start:.2f} сек"
          )