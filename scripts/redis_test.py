import redis

# decode_responses=True means Redis returns Python strings instead of raw bytes
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Basic set/get, just to prove the connection works
r.set("test_key", "hello_sentinel")
value = r.get("test_key")
print(f"Got back: {value}")

# INCR — atomic increment, this is the operation velocity checks actually rely on
r.delete("counter_demo")  # start clean
r.incr("counter_demo")
r.incr("counter_demo")
r.incr("counter_demo")
count = r.get("counter_demo")
print(f"Counter after 3 increments: {count}")