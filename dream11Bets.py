from models.db import getConnection
from models.redis import redisClient


class Dream11Bets:
    dream11_players_table = "dream11_players"

    def __init__(self):
        self.db = getConnection()
        self.redis = redisClient()

    def get_bets(self, user_id):
        """
        fetch dream11 bets
        """
        sql = f"SELECT * FROM dream11_players WHERE user_id = {user_id}"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (1,))
            result = cursor.fetchall()
            print(result)
        return result

    def get_all_users(self):
        """
        fetch all users
        """
        sql = "SELECT COUNT(UNIQUE user_id) FROM dream11_players"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        return result

    def process(self):
        """
        process dream11 bets
        """
        try:
            # Fetch users from database
            bets = self.get_all_users(match_id=1)
            if not bets:
                print("No bets found")
                return

        except Exception as e:
            print(f"Error processing bets: {e}")
        finally:
            self.db.close()
            self.redis.close()
            print("Database and Redis connections closed.")
        # Close the database connection



def main():
    bets = Dream11Bets()
    bets.process()


if __name__ == "__main__":
    main()