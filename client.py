import aiohttp
import asyncio

cities = ['Poletayevo', 'Miass', 'Chelyabinsk']
key = '2a4ff86f9aaa70041ec8e82db64abf56'

# async def main():
#     async with aiohttp.ClientSession() as client:
#         response = await client.get('http://127.0.0.1:8080/test/')
#         data = await response.json()
#         print(data)

# async def main():
#     async with aiohttp.ClientSession() as client:
#         response = await client.post('http://127.0.0.1:8080/weather/',
#                                      json={'cities': cities, 'APPID': key})
#         data = await response.json()
#         print(data)


async def main():
    async with aiohttp.ClientSession() as client:
        # response = await client.post('http://127.0.0.1:8080/user/',
        #                              json={'email': 'Ivan@yandex.ru',
        #                                 'password': '123456',
        #                                 'first_name': 'Иван',
        #                                 'last_name': 'Иванов'})
        #
        # data = await response.json()
        # print(data['answer'])

        # response = await client.get('http://127.0.0.1:8080/user/1')
        #
        # data = await response.json()
        # print(data['answer'])

        response = await client.patch('http://127.0.0.1:8080/user/1',
                                     json={'email': 'Ivan@yandex.ru',
                                        'password': '123456',
                                        'first_name': 'Иван',
                                        'last_name': 'Иванов'})

        data = await response.json()
        print(data['answer'])

asyncio.run(main())
