from config import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_USERNAME

import redis


class RedisClient:

    def __init__(self):
        self.redis = self.connect()
        if(self.redis.ping()):
            print("Redis connection successful")
            print("Redis server version:", r.info("server")["redis_version"])
            return r
        else:
            print("Redis connection failed")
            raise Exception("Redis connection failed")

    def connect(self):
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            username=REDIS_USERNAME,
            password=REDIS_PWD,
        )
        return r;

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        self.redis.set(key, value)

    def delete(self, key):
        self.redis.delete(key)

    def zadd(self, key, value, score):
        res = self.redis.zadd(key, {value: score})
        return res
    
    def zrange(self, key, start, end):
        return self.redis.zrange(key, start, end)

    

    def exists(self, key):
        return self.redis.exists(key)

    def close(self):
        self.redis.close()
        self.redis.connection_pool.disconnect()
        self.redis = None
        print("Redis connection closed")
        return True

    
  
      

