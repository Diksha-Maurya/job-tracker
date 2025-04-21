import redis
import os

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def test_redis():
  try:
        r.set("health_check", "ok")
        return r.get("health_check")
  except Exception as e:
        print("Redis connection failed:", e)
        return False