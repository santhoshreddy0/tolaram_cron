import os
from dotenv import load_dotenv

load_dotenv(".env")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PWD = os.environ.get("DB_PWD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = int(os.environ.get("DB_PORT")) 

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PWD = os.environ.get("REDIS_PWD")
REDIS_USERNAME = os.environ.get("REDIS_USERNAME")