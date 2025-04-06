import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URI = f"postgresql+asyncpg://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    DUMMY_API_KEY = os.getenv("DUMMY_API_KEY")
