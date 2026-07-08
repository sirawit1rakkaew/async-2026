from time import sleep, ctime, time, process_time
import multiprocessing
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name, result_queue):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ
    print(f"Finished making coffee for {customer_name} at {ctime()}")
    result_queue.put(f"Coffee for {customer_name} is ready!")

def main():
    customers = ["Alice", "Bob", "Charlie"]
    result_queue = multiprocessing.Queue()
    processes = []
    
    for customer in customers:
        process = multiprocessing.Process(target=make_coffee, args=(customer, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not result_queue.empty():
        print(result_queue.get())

if __name__ == "__main__":
    main()
    