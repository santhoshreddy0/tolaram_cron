from models.db import getConnection

def print_users_table_columns():
    db = getConnection()
    with db.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM users")
        columns = cursor.fetchall()
        print("📋 Columns in 'users' table:")
        for col in columns:
            print(f"- {col['Field']}")
    db.close()

if __name__ == "__main__":
    print_users_table_columns()
