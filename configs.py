import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

if not token:
    raise ValueError("Нет токена. Проверь авторизацию.")