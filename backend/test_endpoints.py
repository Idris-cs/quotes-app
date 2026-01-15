#!/usr/bin/env python
"""
Test script to verify the Quotes App is working correctly
Run this after starting the Flask server to validate all endpoints
"""

import requests
import json
import sys
import time

BASE_URL = 'http://localhost:5000'
TIMEOUT = 5

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(message, status='info'):
    colors = {
        'info': Colors.BLUE,
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW
    }
    color = colors.get(status, Colors.BLUE)
    print(f"{color}[{status.upper()}]{Colors.END} {message}")

def test_server_running():
    """Test if server is running"""
    print_status("Checking if server is running...", 'info')
    try:
        response = requests.get(f'{BASE_URL}/', timeout=TIMEOUT)
        print_status(f"Server is running (status: {response.status_code})", 'success')
        return True
    except requests.exceptions.ConnectionError:
        print_status(f"Cannot connect to {BASE_URL}", 'error')
        print_status("Make sure to run 'python run.py' from the backend directory", 'warning')
        return False
    except Exception as e:
        print_status(f"Error: {e}", 'error')
        return False

def test_endpoint(name, endpoint, method='GET', expected_status=200):
    """Test an API endpoint"""
    print_status(f"Testing {name}...", 'info')
    try:
        url = f'{BASE_URL}{endpoint}'
        if method == 'GET':
            response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == expected_status:
            print_status(f"✓ {name} - Status {response.status_code}", 'success')
            
            # Try to parse JSON
            try:
                data = response.json()
                print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"  Response (non-JSON): {response.text[:100]}...")
            
            return True
        else:
            print_status(f"✗ {name} - Expected {expected_status}, got {response.status_code}", 'error')
            print(f"  Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print_status(f"✗ {name} - Request timeout", 'error')
        return False
    except Exception as e:
        print_status(f"✗ {name} - Error: {e}", 'error')
        return False

def test_random_quote():
    """Test random quote endpoint"""
    print_status("Testing /api/quotes/random...", 'info')
    try:
        response = requests.get(f'{BASE_URL}/api/quotes/random', timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if 'text' in data and 'author' in data:
                print_status("✓ Random quote endpoint - Success", 'success')
                print(f"  Quote: \"{data['text'][:80]}...\"")
                print(f"  Author: {data['author']}")
                print(f"  Category: {data.get('category', 'N/A')}")
                return True
            else:
                print_status("✗ Random quote - Missing required fields", 'error')
                return False
        else:
            print_status(f"✗ Random quote - Status {response.status_code}", 'error')
            return False
    except Exception as e:
        print_status(f"✗ Random quote - Error: {e}", 'error')
        return False

def test_search():
    """Test search endpoint"""
    print_status("Testing /api/search...", 'info')
    try:
        response = requests.get(f'{BASE_URL}/api/search?q=success', timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if 'quotes' in data:
                count = len(data['quotes'])
                print_status(f"✓ Search endpoint - Found {count} quotes", 'success')
                if count > 0:
                    print(f"  First result: \"{data['quotes'][0]['text'][:80]}...\"")
                return True
            else:
                print_status("✗ Search - Missing quotes field", 'error')
                return False
        else:
            print_status(f"✗ Search - Status {response.status_code}", 'error')
            return False
    except Exception as e:
        print_status(f"✗ Search - Error: {e}", 'error')
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("QUOTES APP - ENDPOINT TEST SUITE")
    print(f"{'='*60}{Colors.END}\n")
    
    results = []
    
    # Test server
    if not test_server_running():
        print_status("Cannot continue without running server", 'error')
        sys.exit(1)
    
    time.sleep(1)  # Give server a moment
    
    # Test endpoints
    print(f"\n{Colors.BLUE}Testing API Endpoints:{Colors.END}\n")
    
    results.append(('Homepage', test_endpoint('Homepage', '/', expected_status=200)))
    time.sleep(0.5)
    
    results.append(('Random Quote API', test_random_quote()))
    time.sleep(0.5)
    
    results.append(('Search API', test_search()))
    time.sleep(0.5)
    
    results.append(('Categories', test_endpoint('Categories (Home Page)', '/', expected_status=200)))
    time.sleep(0.5)
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = 'success' if result else 'error'
        symbol = '✓' if result else '✗'
        print_status(f"{symbol} {test_name}", status)
    
    print(f"\n{Colors.BLUE}Results: {Colors.GREEN}{passed}/{total} tests passed{Colors.END}\n")
    
    if passed == total:
        print_status("All tests passed! Your app is working correctly.", 'success')
        sys.exit(0)
    else:
        print_status(f"{total - passed} test(s) failed. Check the errors above.", 'error')
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_status("Tests interrupted by user", 'warning')
        sys.exit(1)
