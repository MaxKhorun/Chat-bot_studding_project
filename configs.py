import os
from dotenv import load_dotenv

load_dotenv()

# get actual devices list
SOCKET_ID = os.getenv("plug_1")
NIGHT_LAMP_ID = os.getenv("nochnik")
OFFICE_LAMP_ID = os.getenv("office_light")
VACUUM_ID = os.getenv("vacuum")
HUMIDIFIER_ID = os.getenv("humi")
MINI_YA = os.getenv("mini_station")
BIG_YA = os.getenv("big_station")

# get tokens
token = os.getenv("TOKEN")
YA_TOKEN = os.getenv("YA_TOKEN")

for name, value in {
    "BOT TOKEN": token,
    "YA_TOKEN": YA_TOKEN,
}.items():
    if not value:
        raise ValueError(f"Что-то с токеном {name}")
