import time
import random
import math
import redis


##
# Class: Semaphore
# Stores all the information of a Semaphore Agreement
# Provides an interace for trying to access a semaphore
class Semaphore:

    def __init__(self, manager, key, max_locks=1, expire_time=None):
        self._token         = "%f.%d" % (time.time(), math.floor(random.random()*1000000))
        self._key           = key
        self._mngr          = manager
        self._max           = max_locks
        self._expire_time   = expire_time

    # Tries to get a semaphore, if it fails
    # The thread will wait a random time before trying again
    # The method will only return once the semaphore is granted
    def lock(self):
        lock_granted = False
        while not self._mngr.lock_semaphore(self):
            time.sleep(random.random()*10)

    # Tries to get a lock in a non-blocking way
    # returns True if the lock was granted, or False otherwise
    def try_lock(self):
        return self._mngr.lock_semaphore(self)

    def unlock(self):
        self._mngr.unlock_semaphore(self)

    def key(self):
        return self._key

    def max_locks(self):
        return self._max

    def token(self):
        return self._token

    def expire_time(self):
        return self._expire_time
