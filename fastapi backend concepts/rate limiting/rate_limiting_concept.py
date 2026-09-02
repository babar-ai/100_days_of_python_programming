import time
from collections import deque, defaultdict
import threading

class TokenBucket:
    """
    Token Bucket Algorithm:
    - Bucket holds a maximum number of tokens.
    - Tokens are added at a constant rate.
    - Each request consumes 1 token. If empty, request is denied.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.last_refill = now
            
            # Refill tokens based on elapsed time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False


class LeakyBucket:
    """
    Leaky Bucket Algorithm:
    - Requests enter a queue (bucket) of fixed capacity.
    - Requests are processed at a constant rate.
    - If the bucket overflows, requests are dropped.
    """
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate  # requests per second
        self.water = 0.0
        self.last_time = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            self.last_time = now
            
            # Leak water (process requests) over time
            self.water = max(0.0, self.water - elapsed * self.leak_rate)
            
            if self.water + 1.0 <= self.capacity:
                self.water += 1.0
                return True
            return False


class FixedWindowCounter:
    """
    Fixed Window Counter Algorithm:
    - Divides timeline into fixed-size windows (e.g., 1 minute).
    - Counts requests in the current window.
    - Resets count at the start of each new window.
    """
    def __init__(self, limit: int, window_size_seconds: int):
        self.limit = limit
        self.window_size = window_size_seconds
        self.current_window = int(time.time()) // self.window_size
        self.counter = 0
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            window = int(now) // self.window_size
            
            if window != self.current_window:
                self.current_window = window
                self.counter = 0
                
            if self.counter < self.limit:
                self.counter += 1
                return True
            return False


class SlidingWindowLog:
    """
    Sliding Window Log Algorithm:
    - Keeps a timestamp log of all requests.
    - Drops timestamps older than the sliding window.
    - If the number of timestamps within the window < limit, allow request.
    """
    def __init__(self, limit: int, window_size_seconds: int):
        self.limit = limit
        self.window_size = window_size_seconds
        self.timestamps = deque()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            
            # Remove timestamps outside the current window
            while self.timestamps and self.timestamps[0] <= now - self.window_size:
                self.timestamps.popleft()
                
            if len(self.timestamps) < self.limit:
                self.timestamps.append(now)
                return True
            return False


class SlidingWindowCounter:
    """
    Sliding Window Counter Algorithm:
    - Combines Fixed Window Counter with Sliding Window Log approximation.
    - Calculates weighted count based on previous and current window.
    """
    def __init__(self, limit: int, window_size_seconds: int):
        self.limit = limit
        self.window_size = window_size_seconds
        self.counters = defaultdict(int)
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            current_window = int(now) // self.window_size
            previous_window = current_window - 1
            
            # Time elapsed in current window
            current_window_time_offset = now % self.window_size
            weight = (self.window_size - current_window_time_offset) / self.window_size
            
            # Estimated requests in sliding window
            count = (self.counters[previous_window] * weight) + self.counters[current_window]
            
            if count < self.limit:
                self.counters[current_window] += 1
                return True
            return False


if __name__ == "__main__":
    print("=== Testing Rate Limiter Algorithms ===")

    def test_limiter(name, limiter, requests=5, interval=0.1):
        print(f"\n--- Testing {name} ---")
        for i in range(1, requests + 1):
            allowed = limiter.allow_request()
            status = "✅ Allowed" if allowed else "❌ Blocked"
            print(f"Request {i}: {status:<12} (Time: {time.strftime('%X')})")
            time.sleep(interval)

    # 1. Token Bucket: Capacity 3, Refill 2 tokens/sec
    tb = TokenBucket(capacity=3, refill_rate=2.0)
    test_limiter("Token Bucket", tb, requests=5, interval=0.1)

    # 2. Leaky Bucket: Capacity 3, Leak 2 requests/sec
    lb = LeakyBucket(capacity=3, leak_rate=2.0)
    test_limiter("Leaky Bucket", lb, requests=5, interval=0.1)

    # 3. Fixed Window Counter: Limit 3, Window 1 second
    fw = FixedWindowCounter(limit=3, window_size_seconds=1)
    test_limiter("Fixed Window Counter", fw, requests=5, interval=0.1)

    # 4. Sliding Window Log: Limit 3, Window 1 second
    swl = SlidingWindowLog(limit=3, window_size_seconds=1)
    test_limiter("Sliding Window Log", swl, requests=5, interval=0.1)

    # 5. Sliding Window Counter: Limit 3, Window 1 second
    swc = SlidingWindowCounter(limit=3, window_size_seconds=1)
    test_limiter("Sliding Window Counter", swc, requests=5, interval=0.1)
