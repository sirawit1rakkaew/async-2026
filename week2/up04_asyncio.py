import asyncio
from time import ctime, perf_counter


CUSTOMERS = ("A", "B", "C")
MAKE_COFFEE_SECONDS = 1.0
UPDATE_LCD_SECONDS = 1.0


def log(message):
    print(f"{ctime()} | {message}", flush=True)


async def make_coffee(customer):
    log(f"Making coffee for {customer}...")
    await asyncio.sleep(MAKE_COFFEE_SECONDS)
    log(f"Coffee ready for {customer}!")


async def update_lcd(customer):
    log(f"LCD: Processing for customer {customer}...")
    await asyncio.sleep(UPDATE_LCD_SECONDS)
    log(f"LCD: Done for customer {customer}.")


async def serve_customer(customer):
    await make_coffee(customer)
    await update_lcd(customer)


async def run_machine():
    log("=== Asyncio Coffee Machine ===")
    start_time = perf_counter()

    await asyncio.gather(*(serve_customer(customer) for customer in CUSTOMERS))

    total_time = perf_counter() - start_time
    log(f"Total time: {total_time:.2f} seconds")


def main():
    asyncio.run(run_machine())


if __name__ == "__main__":
    main()
