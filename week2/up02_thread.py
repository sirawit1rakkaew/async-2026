from threading import Thread
from time import ctime, perf_counter, sleep


CUSTOMERS = ("A", "B", "C")
MAKE_COFFEE_SECONDS = 1.0
UPDATE_LCD_SECONDS = 1.0


def log(message):
    print(f"{ctime()} | {message}", flush=True)


def make_coffee(customer):
    log(f"Making coffee for {customer}...")
    sleep(MAKE_COFFEE_SECONDS)
    log(f"Coffee ready for {customer}!")


def update_lcd(customer):
    log(f"LCD: Processing for customer {customer}...")
    sleep(UPDATE_LCD_SECONDS)
    log(f"LCD: Done for customer {customer}.")


def serve_customer(customer):
    make_coffee(customer)
    update_lcd(customer)


def main():
    log("=== Multi-threading Coffee Machine ===")
    start_time = perf_counter()

    threads = [
        Thread(target=serve_customer, args=(customer,), name=f"Customer-{customer}")
        for customer in CUSTOMERS
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    total_time = perf_counter() - start_time
    log(f"Total time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
