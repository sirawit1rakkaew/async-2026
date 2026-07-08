from time import sleep, ctime, time

def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1)
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    
    update_cup_number(customer_name)

def main():
    start_time = time()
    print(f"{ctime()} | === Synchronous Coffee Machine ===")
    
    customers = ["A", "B", "C"]
    for customer in customers:
        make_coffee(customer)
        
    print(f"{ctime()} | Total time: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()