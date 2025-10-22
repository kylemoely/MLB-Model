from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

### Local Dev
# DB_USER = os.getenv("DB_USER")
# DB_NAME = os.getenv("DB_NAME")
# DB_PORT = os.getenv("DB_PORT")
# DB_HOST = os.getenv("DB_HOST")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

### AWS Dev
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
