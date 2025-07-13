#!/usr/bin/env python3
'''Test script for web caching functionality.
'''
import time
import requests
from web import get_page, REDIS_AVAILABLE

def test_caching():
    '''Test the caching functionality with a slow URL.'''
    print("Testing web caching functionality...")
    print(f"Redis available: {REDIS_AVAILABLE}")
    
    # Test URL that simulates a slow response
    url = "http://slowwly.robertomurray.co.uk/delay/2000/url/http://www.google.com"
    
    print(f"\nTesting URL: {url}")
    
    # First request - should be slow
    print("\n1. First request (should be slow):")
    start_time = time.time()
    try:
        result1 = get_page(url)
        end_time = time.time()
        print(f"   Time taken: {end_time - start_time:.2f} seconds")
        print(f"   Response length: {len(result1)} characters")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Second request - should be fast if cached
    print("\n2. Second request (should be fast if cached):")
    start_time = time.time()
    try:
        result2 = get_page(url)
        end_time = time.time()
        print(f"   Time taken: {end_time - start_time:.2f} seconds")
        print(f"   Response length: {len(result2)} characters")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Check if responses are the same
    if result1 == result2:
        print("   ✓ Responses are identical (caching working)")
    else:
        print("   ✗ Responses differ (caching may not be working)")
    
    # Test with a different URL
    print("\n3. Testing with a different URL:")
    url2 = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.github.com"
    start_time = time.time()
    try:
        result3 = get_page(url2)
        end_time = time.time()
        print(f"   Time taken: {end_time - start_time:.2f} seconds")
        print(f"   Response length: {len(result3)} characters")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_caching() 