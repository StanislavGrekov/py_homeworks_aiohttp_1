import aiohttp
import asyncio

# Города, по которым необходимо получить данные о погоде
cities = ['Poletayevo', 'Miass', 'Chelyabinsk']
# Ключ для работы сервиса openweathermap
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
        #Создание пользователя
        # response = await client.post('http://127.0.0.1:8080/user/',
        #                              json={'email': 'dimon@yandex.ru',
        #                                 'password': '12345678',
        #                                 'first_name': 'Дмитрий',
        #                                 'last_name': 'Дмитриев'})
        #
        # data = await response.json()
        # print(data['answer'])

        # Получение пользователя
        # response = await client.get('http://127.0.0.1:8080/user/7')
        #
        # data = await response.json()
        # print(data['answer'])

        # Редактирование пользователя
        # response = await client.patch('http://127.0.0.1:8080/user/7',
        #                              json={'email': 'dimon@yandex.ru',
        #                                 'oldpassword': '12345678',
        #                                 'newpassword': 'password',
        #                                 'first_name': 'Дмитрий',
        #                                 'last_name': 'Дмитриев'})
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

        # Создание записей в БД, содержащих данные о погоде в указаных городах
        # response = await client.post('http://127.0.0.1:8080/weather/',
        #                              json={'cities': cities,
        #                                    'APPID': key,
        #                                    'email': 'dimon@yandex.ru',
        #                                     'password': '12345678',
        #                                    })
        # data = await response.json()
        # print(data['answer'])

        # Получение даyных о погоде из БД по email
        # response = await client.get('http://127.0.0.1:8080/weather/',
        #                              json={
        #                                    'email': 'dimon@yandex.ru',
        #                                    })
        # data = await response.json()
        # for element in data['answer']:
        #     print(element)

        # Удаление записей о погоде
        response = await client.delete('http://127.0.0.1:8080/weather/9',
                                       json={'email': 'dimon@yandex.ru',
                                             'password': '12345678',})

        data = await response.json()
        print(data['answer'])

asyncio.run(main())
