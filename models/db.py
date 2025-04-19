import pymysql
from config import DB_HOST, DB_USER, DB_PWD, DB_NAME, DB_PORT;

def getConnection(autoCommit=True):
    print("Connecting to database...")
    conn = pymysql.Connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PWD,
        database=DB_NAME,
        port=DB_PORT,
        autocommit=autoCommit,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connected to database")
    return conn
