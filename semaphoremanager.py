from semaphore import Semaphore
import redis

class SemaphoreManager:

    # Initializes the Semaphore Manager (dependent of a RedisGroup)
    # It also selects a unique token used to identify its locks
    # @param redis_group RedisGroup object initialized with pool of connections to one or more server
    def __init__(self, redis_group):
        self._group      = redis_group
        self._semaphores = {}


    def open_semaphore(self, key, max_simultaneous_locks=1, expire_time=None):
        self._semaphores[key] = Semaphore(self, key=key, max_locks=max_simultaneous_locks, expire_time=expire_time)
        return self._semaphores[key]

    def lock_semaphore(self, semaphore):
        locks_granted   = 0
        conns           = self._group.connections()
        for conn in conns:
            if self._lock_semaphore_redis(conn, semaphore):
                locks_granted += 1

        # Locks needs to be granted on most of the servers
        # Otherwise, any granted lock must be released and
        # a random sleep time should be applied
        lock_granted = (locks_granted > (len(conns)/2.0))

        if not lock_granted:
            self.unlock_semaphore(semaphore)

        return lock_granted

    def unlock_semaphore(self, semaphore):
        conns = self._group.connections()
        for conn in conns:
            self._unlock_semaphore_redis(conn, semaphore)


    # PRIVATE METHODS

    def _lock_semaphore_redis(self, server, semaphore):
        key     = semaphore.key()
        token   = semaphore.token()
        max_key = semaphore.max_locks()
        try:
            for i in range(max_key):
                pkey = "lockpact_%s.%d" % (key, i)
                if server.setnx(pkey, token):
                    if semaphore.expire_time():
                        server.setex(pkey, token, semaphore.expire_time())
                    return True
        except redis.exceptions.ConnectionError:
            print "Could not get lock from redis server (ConnectionError). Skipping to next server."
        return False

    def _unlock_semaphore_redis(self, server, semaphore):
        key     = semaphore.key()
        token   = semaphore.token()
        max_key = semaphore.max_locks()
        try:
            for i in range(max_key):
                pkey = "lockpact_%s.%d" % (key, i)
                unlock_script = """
                    if redis.call("get",KEYS[1]) == ARGV[1]
                    then
                        return redis.call("del",KEYS[1])
                    else
                        return 0
                    end
                """
                server.eval(unlock_script, 1, pkey, token)
        except redis.exceptions.ConnectionError:
            # print "Could not unlock key from redis server (ConnectionError). Skipping to next server."
            return False
        return True
