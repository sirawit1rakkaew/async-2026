from time import sleep, ctime, time
import multiprocessing

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน 
def make_coffee(customer_name):
    print(f"Start making coffee for {customer_name} at {ctime()}")
    sleep(3)  # จำลองเวลาที่ใช้ในการทำกาแฟ
    print(f"Finished making coffee for {customer_name} at {ctime()}")

def main():
    customers = ["Alice", "Bob", "Charlie"]
    processes = []
    for customer in customers:
        process = multiprocessing.Process(target=make_coffee, args=(customer,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

# สิ่งสำคัญที่สุดสำหรับ Multi-processing ใน Python: ต้องครอบด้วยบล็อกนี้เสมอ
if __name__ == "__main__":
    main()
    