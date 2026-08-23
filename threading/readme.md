# 🧵 Threading & Multithreading in Python — Interview Notes

---

## 1. What is a Thread?

A **thread** is the smallest unit of execution within a process. A single process can have multiple threads running concurrently, sharing the same memory space.

```
Process
 ├── Thread 1  (main thread)
 ├── Thread 2
 └── Thread 3
```

---

## 2. Process vs Thread

| Feature        | Process                        | Thread                        |
|----------------|--------------------------------|-------------------------------|
| Memory         | Separate memory space          | Shared memory space           |
| Creation cost  | Heavy (slow to create)         | Lightweight (fast to create)  |
| Communication  | IPC (pipes, sockets, etc.)     | Shared variables directly     |
| Crash effect   | Doesn't affect other processes | Can crash the entire process  |
| Example        | Running two Python scripts     | Two functions in one script   |

---

## 3. Concurrency vs Parallelism

| Term          | Meaning                                                                 |
|---------------|-------------------------------------------------------------------------|
| **Concurrency** | Multiple tasks make progress, but not necessarily at the same instant (switching rapidly) |
| **Parallelism** | Multiple tasks run at the **exact same time** on multiple CPU cores    |

> 🔑 Python threads give **concurrency**, NOT true parallelism (due to the GIL).

---

## 4. The GIL — Global Interpreter Lock

The **GIL** is a mutex (lock) in CPython that allows only **one thread to execute Python bytecode at a time**, even on a multi-core CPU.

### Why does it exist?
- To protect Python's memory management (reference counting) from race conditions.

### Impact:
- **CPU-bound tasks** → Threading does NOT help (use `multiprocessing` instead).
- **I/O-bound tasks** → Threading DOES help (GIL is released during I/O waits like `time.sleep()`, file reads, network calls).

```python
# I/O-bound: threading helps ✅
# CPU-bound: threading does NOT help ❌ → use multiprocessing
```

---

## 5. Creating Threads in Python

```python
import threading

def worker():
    print("Thread running")

# Method 1: Pass target function
t = threading.Thread(target=worker)
t.start()
t.join()  # Wait for thread to finish

# Method 2: Subclassing Thread
class MyThread(threading.Thread):
    def run(self):
        print("Thread running via subclass")

t = MyThread()
t.start()
t.join()
```

---

## 6. `start()` vs `run()` vs `join()`

| Method     | What it does                                                    |
|------------|-----------------------------------------------------------------|
| `start()`  | Launches the thread in a **new thread of execution**           |
| `run()`    | Executes the thread's logic in the **current thread** (no new thread created!) |
| `join()`   | Blocks the calling thread until the target thread **finishes** |

> ⚠️ Always use `start()`, never call `run()` directly if you want actual threading.

---

## 7. Daemon Threads

A **daemon thread** runs in the background and is **automatically killed** when the main program exits.

```python
t = threading.Thread(target=worker, daemon=True)
t.start()

# Main program exits → daemon thread is killed automatically
```

| Type           | Behavior on main exit          |
|----------------|--------------------------------|
| Normal thread  | Main waits for it to finish    |
| Daemon thread  | Killed immediately when main exits |

---

## 8. Thread Synchronization — Race Conditions

A **race condition** occurs when two threads access and modify shared data simultaneously, leading to unpredictable results.

```python
# BAD: race condition
counter = 0
def increment():
    global counter
    counter += 1  # Not atomic! Read-modify-write can interleave
```

---

## 9. Lock (Mutex)

A **Lock** ensures only one thread accesses a critical section at a time.

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:        # Acquires lock, releases automatically
        counter += 1  # Critical section — thread-safe ✅
```

### Lock methods:
| Method        | Description                                      |
|---------------|--------------------------------------------------|
| `lock.acquire()` | Blocks until the lock is free, then acquires |
| `lock.release()` | Releases the lock                            |
| `with lock:`  | Recommended — auto acquire & release (safer)     |

---

## 10. RLock (Re-entrant Lock)

A **RLock** can be acquired multiple times by the **same thread** (useful in recursive functions).

```python
rlock = threading.RLock()

def recursive(n):
    with rlock:  # Can be acquired again by the same thread
        if n > 0:
            recursive(n - 1)
```

> A regular `Lock` would **deadlock** if the same thread tries to acquire it twice.

---

## 11. Deadlock

A **deadlock** occurs when two or more threads are waiting on each other to release a lock — and none can proceed.

```
Thread 1 holds Lock A, waits for Lock B
Thread 2 holds Lock B, waits for Lock A
→ Both wait forever = Deadlock ☠️
```

**Prevention tips:**
- Always acquire locks in the same order.
- Use `timeout` in `lock.acquire(timeout=5)`.
- Use `RLock` where needed.

---

## 12. Event — Thread Signaling

A **threading.Event** is used to signal between threads (flag-based communication).

```python
import threading, time

done = threading.Event()

def worker():
    while not done.is_set():
        print("Working...")
        time.sleep(1)

t = threading.Thread(target=worker)
t.start()

input("Press Enter to stop: ")
done.set()   # Signal the thread to stop
t.join()
```

| Method         | Description                          |
|----------------|--------------------------------------|
| `event.set()`    | Sets the flag (signals all waiting threads) |
| `event.clear()` | Resets the flag                      |
| `event.is_set()` | Returns True if flag is set         |
| `event.wait()`   | Blocks until the flag is set        |

---

## 13. Semaphore

A **Semaphore** limits the number of threads that can access a resource simultaneously.

```python
semaphore = threading.Semaphore(3)  # Max 3 threads at a time

def worker():
    with semaphore:
        print("Accessing resource")
        time.sleep(2)
```

> Use case: Limiting concurrent database connections, API rate limiting.

---

## 14. ThreadPoolExecutor (Modern Approach)

`concurrent.futures.ThreadPoolExecutor` is the modern, high-level way to manage threads.

```python
from concurrent.futures import ThreadPoolExecutor

def task(n):
    return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
    mylist = [1, 2, 3, 4, 5]
    results = executor.map(task, mylist)
    print(list(results))  # [1, 4, 9, 16, 25]
```

### `submit()` vs `map()`

| Method      | Returns           | Use when                              |
|-------------|-------------------|---------------------------------------|
| `map()`     | Iterator of results (ordered) | Same function, multiple inputs |
| `submit()`  | `Future` object   | Different tasks, need individual control |

---

## 15. Multiprocessing vs Threading

| Feature         | `threading`              | `multiprocessing`            |
|-----------------|--------------------------|------------------------------|
| GIL affected?   | Yes                      | No (separate processes)      |
| Best for        | I/O-bound tasks          | CPU-bound tasks               |
| Memory          | Shared                   | Separate (no sharing by default) |
| Overhead        | Low                      | High                          |
| Module          | `threading`              | `multiprocessing`             |

```python
# CPU-bound → use multiprocessing
from multiprocessing import Process

p = Process(target=heavy_computation)
p.start()
p.join()
```

---

## 16. Thread-Local Storage

**`threading.local()`** gives each thread its own independent copy of a variable.

```python
local_data = threading.local()

def worker():
    local_data.value = threading.current_thread().name
    print(local_data.value)  # Each thread sees its own value
```

---

## 17. Common Interview Questions

| Question | Short Answer |
|---|---|
| What is the GIL? | A lock allowing only one thread to run Python bytecode at a time |
| Threading for CPU-bound tasks? | No — use `multiprocessing` |
| Threading for I/O-bound tasks? | Yes — GIL is released during I/O |
| What is a race condition? | Two threads modify shared data simultaneously causing unpredictable results |
| How to prevent race conditions? | Use `Lock`, `RLock`, or `Semaphore` |
| Daemon thread vs normal thread? | Daemon is killed when main exits; normal thread keeps main alive |
| `join()` purpose? | Makes the calling thread wait until the target thread finishes |
| `Event` vs `Lock`? | Event is for signaling between threads; Lock is for mutual exclusion |
| What is deadlock? | Circular waiting on locks — threads block each other forever |
| Best modern threading API? | `concurrent.futures.ThreadPoolExecutor` |

---

## 18. Quick Reference — threading Module

```python
import threading

threading.Thread(target=fn, args=(), daemon=False)  # Create thread
threading.Lock()          # Mutual exclusion
threading.RLock()         # Re-entrant lock
threading.Event()         # Flag-based signaling
threading.Semaphore(n)    # Limit concurrent access
threading.local()         # Thread-local storage
threading.current_thread()# Get current thread object
threading.active_count()  # Number of active threads
threading.enumerate()     # List all active threads
```

---

*Last updated: 2026-07-18 | For interview revision use only*
