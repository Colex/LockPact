from redisgroup import RedisGroup
from semaphoremanager import SemaphoreManager
import redis
import time

class LockPact:

    # Initializes the module and the pool of connections to all Redis instances
    # @param redis Dictionary or Array of Dictionaries specifying host and port
    def __init__(self, redis):
        if not type(redis) in [dict, list]:
            raise Exception("Unsupported variable type on LockPact initializer")

        # If a hash was given, convert into a list of single element
        redis_group = [redis] if type(redis) is dict else redis

        # Initialize Redis Group Pool
        self._redis_group = RedisGroup(redis_group)

        # Initialize the semaphore on the created group
        self._semaphore_mngr = SemaphoreManager(self._redis_group)

    def agree(self, key, max_simultaneous_locks=1, expire_time=None):
        return self._semaphore_mngr.open_semaphore(key, max_simultaneous_locks, expire_time)


if __name__ == "__main__":
    #Example
    pact = LockPact([{'host': 'localhost'}])
    semaphore = pact.agree("redshift", expire_time=10)
    semaphore.lock()
    #time.sleep(5)
    #semaphore.unlock()
