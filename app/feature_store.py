import redis
r= redis.Redis(host="localhost", port=6379, decode_responses=True)

WINDOW_SECONDS=60

def record_transaction(user_id:str) -> int:
    """
    Increments this user's transaction count for the current 60-second window
    and returns the updated count. Uses a Redis key that auto-expires, so we
    never need a separate cleanup process.
    """
    key=f"txn_count:{user_id}"
    count= r.incr(key)

    if count==1:
        r.expire(key, WINDOW_SECONDS)
    return count

def get_transaction_count(user_id:str) -> int:
        
    """ Returns the user's current transaction count in the active window, or 0. """
    key = f"txn_count:{user_id}"
    value= r.get(key)
    return int(value) if value else 0

