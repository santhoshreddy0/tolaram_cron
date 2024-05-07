import os
import pymysql
from dotenv import load_dotenv

load_dotenv(".env")


def getConnection(autoCommit=True):

    conn = pymysql.Connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PWD"),
        database=os.environ.get("DB_NAME"),
        autocommit=autoCommit,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
