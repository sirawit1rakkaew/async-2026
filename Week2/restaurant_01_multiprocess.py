from time import sleep, ctime, time
import multiprocessing

# 1. ขั้นตอนต้อนรับหน้าร้าน ทำแบบ Synchronous
def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# 2. กระบวนการส่วนตัวของลูกค้าแต่ละคน ที่จะถูกนำไปรันในแต่ละ Process
def customer_private_workflow(customer):
    # Take Order
    print(f"{ctime()} [Process-{customer}] Taking Order ...")
    sleep(1)
    print(f"{ctime()} [Process-{customer}] Taking Order ...Done!")

    # Do Cooking
    print(f"{ctime()} [Process-{customer}] Cooking Spaghetti ...")
    sleep(1)
    print(f"{ctime()} [Process-{customer}] Cooking Spaghetti ...Done!")

    # Manage Bar
    print(f"{ctime()} [Process-{customer}] Manage Bar for Drink ...")
    sleep(1)
    print(f"{ctime()} [Process-{customer}] Manage Bar for Drink ...Done!")
    print(f"{ctime()} [Process-{customer}] All served!\n")

if __name__ == "__main__":
    customers = ['A', 'B', 'C']
    start_time = time()

    # PHASE 1: Greet ลูกค้าทีละคน (Synchronous)
    for customer in customers:
        greet_diners(customer)

    print(f"\n{ctime()} --- All customers greeted. Branching out into independent Processes! ---\n")

    # PHASE 2: แยกสาขา (Processes) ให้ลูกค้าแต่ละคน
    processes = []
    for customer in customers:
        # ใช้ multiprocessing.Process แทน threading.Thread
        p = multiprocessing.Process(target=customer_private_workflow, args=(customer,))
        processes.append(p)
        p.start() # สั่งให้ Process เริ่มทำงานขนานกันจริงๆ บน CPU คนละ Core

    # รอให้ทุก Process ทำงานเสร็จ
    for p in processes:
        p.join()

    duration = time() - start_time
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")