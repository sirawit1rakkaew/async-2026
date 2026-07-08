import time

# งานแต่ละอย่าง (ใช้ time.sleep() เพราะเป็นแบบ Blocking/Synchronous)
def greet_customer(customer):
    print(f"{time.ctime()} -> Greeting for {customer}...")
    time.sleep(1)
    print(f"{time.ctime()} -> Greeting for {customer}...Done!")

def take_order(customer):
    print(f"{time.ctime()} -> Taking order for {customer}")
    time.sleep(1)
    print(f"{time.ctime()} -> Order taken for {customer}")

def cook_food(customer):
    print(f"{time.ctime()} -> Cooking for {customer}")
    time.sleep(1)
    print(f"{time.ctime()} -> Cooking for {customer}...Done!")

def serve_drink(customer):
    print(f"{time.ctime()} -> Preparing drink for {customer}")
    time.sleep(1)
    print(f"{time.ctime()} -> Drink served for {customer}")

def main():
    start_time = time.time()
    customers = ["Customer-A", "Customer-B", "Customer-C"]
    
    for customer in customers:
        # ทำงานเรียงลำดับไปทีละขั้นตอน
        greet_customer(customer)
        take_order(customer)
        cook_food(customer)
        serve_drink(customer)
        print(f"{customer} served.")

    print(f"Finished Entire Restaurant Operation in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()