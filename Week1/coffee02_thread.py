from time import sleep, ctime, time
import threading

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ
    print(f"Finished making coffee for {customer_name} at {ctime()}")

def main():
    # คิวลูกค้า
    customers = ["Alice", "Bob", "Charlie"]
    threads = []
    for customer in customers:
        thread = threading.Thread(target=make_coffee, args=(customer,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# สั่งให้โปรแกรมทำงาน
if __name__ == "__main__":
    main()    