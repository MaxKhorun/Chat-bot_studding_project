import traceback

from configs import YA_TOKEN
import aiohttp
import asyncio

# async def get_devices():
#     url = "https://api.iot.yandex.net/v1.0/user/info"
#     headers = {"Authorization": f"Bearer {YA_TOKEN}"}
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as resp:
#             data = await resp.json()
#             for device in data.get("devices", []):
#                 print(f"Имя: {device['name']}, ID: {device['id']}")

async def get_devices_info():
    url = "https://api.iot.yandex.net/v1.0/user/info"
    headers = {"Authorization": f"Bearer {YA_TOKEN}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                # Выбрасываем исключение с деталями
                raise Exception(f"Ошибка API {resp.status}: {error_text}")
            return await resp.json()

if __name__ == "__main__":
    try:
        # Запускаем асинхронную функцию и ждём результат
        result = asyncio.run(get_devices_info())
        print("Успех! Получены данные:")
        print(result)
    except Exception as e:
        # Печатаем полную информацию об ошибке
        print("❌ Произошла ошибка:")
        print(e)
        # Если нужно увидеть полный стек вызовов (для сложных ошибок)
        traceback.print_exc()
#
# async def get_devices():
#     url = "https://api.iot.yandex.net/v1.0/user/info"
#     headers = {"Authorization": f"Bearer {YA_TOKEN}"}
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as resp:
#             if resp.status != 200:
#                 print(f"Ошибка {resp.status}: {await resp.text()}")
#                 return
#             data = await resp.json()
#             devices = data.get("devices", [])
#             if not devices:
#                 print("Устройства не найдены.")
#                 return
#             print("Найденные устройства:")
#             for device in devices:
#                 print(f"  Имя: {device['name']}, ID: {device['id']}")
#             return devices
#
#
# if __name__ == "__main__":
#     # Запускаем асинхронную функцию
#     asyncio.run(get_devices())