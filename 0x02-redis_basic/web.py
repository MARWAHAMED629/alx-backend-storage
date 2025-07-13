#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable
import time
import threading


# Initialize Redis with error handling
try:
    redis_store = redis.Redis()
    # Test the connection
    redis_store.ping()
    REDIS_AVAILABLE = True
except redis.ConnectionError:
    REDIS_AVAILABLE = False
    redis_store = None

# In-memory cache for fallback when Redis is not available
memory_cache = {}
cache_timestamps = {}
cache_lock = threading.Lock()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        if REDIS_AVAILABLE and redis_store:
            redis_store.incr(f'count:{url}')
            cached_result = redis_store.get(f'result:{url}')
            if cached_result is not None:
                return cached_result.decode('utf-8')
            result = method(url)
            redis_store.setex(f'result:{url}', 10, result)
            return result
        else:
            # Fallback implementation with in-memory cache
            with cache_lock:
                current_time = time.time()
                
                # Check if we have a cached result and it's not expired (10 seconds)
                if url in memory_cache and (current_time - cache_timestamps.get(url, 0)) < 10:
                    return memory_cache[url]
                
                # Get fresh result
                result = method(url)
                
                # Cache the result
                memory_cache[url] = result
                cache_timestamps[url] = current_time
                
                return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text


if __name__ == "__main__":
    # Test with a slow URL as suggested in the task
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"
    
    print("First request (should be slow):")
    start_time = time.time()
    result1 = get_page(url)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    print("\nSecond request (should be fast if cached):")
    start_time = time.time()
    result2 = get_page(url)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    # Check the count if Redis is available
    if REDIS_AVAILABLE and redis_store:
        count = redis_store.get(f'count:{url}')
        print(f"\nURL accessed {count.decode('utf-8') if count is not None else '0'} times")
    else:
        print("\nRedis not available - count tracking disabled")
