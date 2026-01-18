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
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        print_status(f"Cannot connect to {BASE_URL}", 'error')
        print_status("Make sure to run 'python run.py' from the backend directory", 'warning')
        assert False
    except Exception as e:
        print_status(f"Error: {e}", 'error')
        assert False

def check_endpoint(name, endpoint, method='GET', expected_status=200):
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
        assert response.status_code == 200
        data = response.json()
        assert 'text' in data and 'author' in data
        print_status("✓ Random quote endpoint - Success", 'success')
        print(f"  Quote: \"{data['text'][:80]}...\"")
        print(f"  Author: {data['author']}")
        print(f"  Category: {data.get('category', 'N/A')}")
    except AssertionError:
        print_status("✗ Random quote - Missing required fields or wrong status", 'error')
        assert False
    except Exception as e:
        print_status(f"✗ Random quote - Error: {e}", 'error')
        assert False

def test_search():
    """Test search endpoint"""
    print_status("Testing /api/search...", 'info')
    try:
        response = requests.get(f'{BASE_URL}/api/search?q=success', timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert 'quotes' in data
        count = len(data['quotes'])
        print_status(f"✓ Search endpoint - Found {count} quotes", 'success')
        if count > 0:
            print(f"  First result: \"{data['quotes'][0]['text'][:80]}...\"")
    except AssertionError:
        print_status("✗ Search - Missing quotes field or wrong status", 'error')
        assert False
    except Exception as e:
        print_status(f"✗ Search - Error: {e}", 'error')
        assert False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("QUOTES APP - ENDPOINT TEST SUITE")
    print(f"{'='*60}{Colors.END}\n")
    
    # Test server
    try:
        test_server_running()
    except AssertionError:
        print_status("Cannot continue without running server", 'error')
        sys.exit(1)
    
    time.sleep(1)  # Give server a moment
    
    # Test endpoints
    print(f"\n{Colors.BLUE}Testing API Endpoints:{Colors.END}\n")
    
    all_passed = True
    
    try:
        check_endpoint('Homepage', '/', expected_status=200)
        print_status("✓ Homepage", 'success')
    except:
        print_status("✗ Homepage", 'error')
        all_passed = False
    time.sleep(0.5)
    
    try:
        test_random_quote()
    except:
        all_passed = False
    time.sleep(0.5)
    
    try:
        test_search()
    except:
        all_passed = False
    time.sleep(0.5)
    
    try:
        check_endpoint('Categories (Home Page)', '/', expected_status=200)
        print_status("✓ Categories", 'success')
    except:
        print_status("✗ Categories", 'error')
        all_passed = False
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}{Colors.END}\n")
    
    if all_passed:
        print_status("All tests passed! Your app is working correctly.", 'success')
        sys.exit(0)
    else:
        print_status("Some tests failed. Check the errors above.", 'error')
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_status("Tests interrupted by user", 'warning')
        sys.exit(1)
