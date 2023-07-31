import time

def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}
        def wrapper(*args, **kwargs):
            cache_key = (func.__name__,) + tuple(args) + tuple(kwargs.items())
            now = time.time()
            cached_result = cache.get(cache_key)
            if cached_result is None or now - cached_result['timestamp'] > ttl_seconds:
                cached_result = func(*args, **kwargs)
                cache[cache_key] = {'result': cached_result, 'timestamp': now}
                return cached_result
            return cached_result['result']
        return wrapper
    return decorator