import aiohttp
import asyncio

cities = ['Poletayevo', 'Miass', 'Chelyabinsk']
key = '2a4ff86f9aaa70041ec8e82db64abf56'

# async def main():
#     async with aiohttp.ClientSession() as client:
#         response = await client.get('http://127.0.0.1:8080/test/')
#         data = await response.json()
#         print(data)

async def main():
    async with aiohttp.ClientSession() as client:
        response = await client.post('http://127.0.0.1:8080/weather/',
                                     json={'cities': cities, 'APPID': key})
        print(response)

asyncio.run(main())