LockPact Module
---------------------

Module in Python for **distributed scalable semaphores**.
The module introduces an easy interface to keep distributed systems synchronized when accessing a shared resource. It allows creating Counting and Binary semaphores. It also let's you set up a TTL (in case the system accessing the resource fails before unlocking the semaphore).
It uses a **Redis** cluster to keep all systems synchronized.

You may use a combination of Redis nodes, a lock will only be granted if the node is able to get the lock in the majority of the nodes.
```
pact = LockPact([{'host': 'redis1.host.com'}, {'host': 'redis2.host.com'}, {'host': 'redis3.host.com'}])
```

After a lock pact interface is initialized, you can start configuring semaphores by specifying the name, **expire_time** *(default None)* and **max_simultaneous_locks** *(default to 1)*.
```
semaphore = pact.agree("printer", expire_time=10, max_simultaneous_locks=1)
```

Once the semaphore rules are agreed on, you may **lock**, **try_lock**, and **unlock** the semaphore.
```
if (semaphore.try_lock()):
  print("Lock granted")
  use_resource()
else:
  print("Failed to get lock, try until granted...")
  semaphore.lock()
  use_resource()
semaphore.unlock()
```

Full Example:
```
from lockpact import LockPact

pact = LockPact([{'host': 'localhost'}])
semaphore = pact.agree("printer", expire_time=10)
semaphore.lock()
time.sleep(5)
semaphore.unlock()

```

Cross-platform
----------
Although the module is written in Python, it can be easily ported to any other language. This distributed locking system should work regardless of the technologies behind.
