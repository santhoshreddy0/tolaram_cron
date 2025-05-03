from models.db import getConnection
from models.redis import RedisClient
import datetime


class Dream11Bets:

    PLAYER_TABLE = "dream11_players"
    MAPPING_TABLE = "match_player_mapping"
    TOURNAMENTS_TABLE = "tournaments"
    REDIS_LEADERBOARD_KEY = "leaderboard"
    REDIS_LASTUPDATED_KEY = "last_updated"
    REDIS_SCORE_UPDATED_AT_KEY = "score_updated_at"
    REDIS_UPDATE_FLAG_KEY = "update_leaderboard"
    BATCH_LIMIT = 10
    INITIAL_OFFSET = 0

    def __init__(self):
        self.db = getConnection()
        self.redis = RedisClient()
        self.limit = self.BATCH_LIMIT
        self.offset = self.INITIAL_OFFSET

    def should_update_leaderboard(self):
        value = self.redis.get(self.REDIS_UPDATE_FLAG_KEY)
        return value and value == "yes"

    def set_leaderboard_flag_to_no(self):
        self.redis.set(self.REDIS_UPDATE_FLAG_KEY, "no")

    def get_users_batch(self, limit=10, offset=0):
        sql = f"""
            SELECT DISTINCT user_id 
            FROM {self.PLAYER_TABLE}
            LIMIT %s OFFSET %s
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (limit, offset))
            return cursor.fetchall()

    def get_user_points(self, user_id):
        sql = f"""
            SELECT 
              SUM(
                IFNULL(mpm.points, 0) * 
                CASE
                  WHEN dp.role_type = 'captain' THEN 2
                  WHEN dp.role_type = 'vice-captain' THEN 1.5
                  ELSE 1
                END
              ) AS total_points
            FROM {self.PLAYER_TABLE} dp
            LEFT JOIN {self.MAPPING_TABLE} mpm 
              ON dp.player_id = mpm.player_id
            WHERE dp.user_id = %s
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result["total_points"] or 0

    def process_user_batch(self):
        users = self.get_users_batch(limit=self.limit, offset=self.offset)
        if not users:
            return False
        for user in users:
            user_id = user["user_id"]
            total_points = self.get_user_points(user_id)
            print(f"User {user_id} => Points: {total_points}")
            self.redis.zadd(self.REDIS_LEADERBOARD_KEY, user_id, float(total_points))
        self.offset += self.limit
        return True

    def process(self):
        try:
            if not self.should_update_leaderboard():
                print("Leaderboard is already up to date. Updating timestamp only...")
                current_utc = datetime.datetime.now(datetime.UTC)
                self.redis.set(self.REDIS_LASTUPDATED_KEY, current_utc.isoformat())
                print(f"Leaderboard timestamp refreshed at UTC: {current_utc}")
                return

            while self.process_user_batch():
                pass

            current_utc = datetime.datetime.now(datetime.UTC)
            self.redis.set(self.REDIS_LASTUPDATED_KEY, current_utc.isoformat())
            self.redis.set(self.REDIS_SCORE_UPDATED_AT_KEY, current_utc.isoformat())
            print(f"Leaderboard last updated at UTC: {current_utc}")
            self.set_leaderboard_flag_to_no()

        except Exception as e:
            print(f"Error processing bets: {e}")
        finally:
            self.db.close()
            self.redis.close()
            print("Database and Redis connections closed.")


def main():
    bets = Dream11Bets()
    bets.process()


if __name__ == "__main__":
    main()
