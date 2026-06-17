import asyncio

async def cell_url():
    url = 'https://www.google.com'
    response = await asyncio.to_thread(lambda: __import__('requests').get(url))
    return response.text

async def main():
    html = await cell_url()
    print(html[:100])  # พิมพ์แค่ 100 ตัวอักษรแรกของ HTML

if __name__ == "__main__":
    asyncio.run(main())