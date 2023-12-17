from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")
