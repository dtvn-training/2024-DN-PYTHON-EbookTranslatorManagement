from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
