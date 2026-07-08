from time import sleep, ctime, time, process_time
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ
    print(f"Finished making coffee for {customer_name} at {ctime()}")

def main():
    customers = ["Alice", "Bob", "Charlie"]
    threads = []
    for customer in customers:
        thread = threading.Thread(target=make_coffee, args=(customer,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()