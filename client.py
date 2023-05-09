import aiohttp
import asyncio

# Города по которым необходимо получить данные о погоде
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
        # Создание пользователя
        # response = await client.post('http://127.0.0.1:8080/user/',
        #                              json={'email': 'stason@yandex.ru',
        #                                 'password': '12345678',
        #                                 'first_name': 'Stas',
        #                                 'last_name': 'Grekov'})
        #
        # data = await response.json()
        # print(data['answer'])

        # Получение пользователя
        # response = await client.get('http://127.0.0.1:8080/user/2')
        #
        # data = await response.json()
        # print(data['answer'])

        # Редактирование пользователя
        # response = await client.patch('http://127.0.0.1:8080/user/2',
        #                              json={'email': 'semenov@yandex.ru',
        #                                 'oldpassword': '12345678',
        #                                 'newpassword': 'password',
        #                                 'first_name': 'Семен',
        #                                 'last_name': 'Cеменов'})
        #
        # data = await response.json()
        # print(data['answer'])

        # Удаление пользователя
        # response = await client.delete('http://127.0.0.1:8080/user/3',
        #                                json={'email': 'semenov@yandex.ru',
        #                                      'password': '12345678',})
        #
        # data = await response.json()
        # print(data['answer'])

        response = await client.post('http://127.0.0.1:8080/weather/',
                                     json={'cities': cities,
                                           'APPID': key,
                                           'email': 'stason@yandex.ru',
                                            'password': '1234567898',
                                           })
        data = await response.json()
        print(data)

asyncio.run(main())
