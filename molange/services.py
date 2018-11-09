class MessageDeduplicationService:
    REDIS_SET_KEY = 'molange:messages'
    EXPIRATION_TIME = 60 * 60 * 24 * 15

    def __init__(self, redis_connection):
        self._redis_conn = redis_connection

    def is_processed(self, message_id):
        return self._redis_conn.sismember(self.REDIS_SET_KEY, message_id)

    def add(self, message_id):
        self._redis_conn.sadd(self.REDIS_SET_KEY, message_id)
        self._redis_conn.expire(self.REDIS_SET_KEY, self.EXPIRATION_TIME)
