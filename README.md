LockPact Module
---------------------

Module in Python for **distributed scalable semaphores**.
The module introduces an easy interface to keep distributed systems synchronized when accessing a shared resource. It allows creating Counting and Binary semaphores. It also let's you set up a TTL (in case the system accessing the resource fails before unlocking the semaphore).
It uses a **Redis** cluster to keep all systems synchronized.

Example:
```
from lockpact import LockPact

pact = LockPact([{'host': 'localhost'}])
semaphore = pact.agree("printer", expire_time=10)
semaphore.lock() #sempahore.try_lock() for non-blocking behavior
time.sleep(5)
semaphore.unlock()

```
