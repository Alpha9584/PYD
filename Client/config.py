
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv("Service_URL")
WS_BASE_URL = os.getenv("WS")
print(WS_BASE_URL)
