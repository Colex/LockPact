##
# This module is responsible for managing the pool of Redis
import redis

class RedisGroup:

    # Initializes all connections to every redis server
    # @param redis_endpoints Array of Dictionaries specifying host and port for each server
    def __init__(self, redis_endpoints):
        # Initialize the connection pool array
        self._pool = []

        for endpoint in redis_endpoints:
            conn = redis.ConnectionPool(host=endpoint['host'], port=(endpoint.get('port') or 6379), db=(endpoint.get('db') or 0))
            self._pool.append(conn)

    def connections(self):
        conns = []
        for pool in self._pool:
            conns.append(redis.Redis(connection_pool=pool))
        return conns
    
