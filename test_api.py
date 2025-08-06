#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing API for useless facts
"""

import requests
import json

def test_api():
    """Tests various API endpoints"""
    base_url = "https://uselessfacts.jsph.pl/api/v2/facts"
    
    print("Testing API for useless facts\n")
    
    # Test 1: Random fact in English
    print("1. Test: Random fact in English")
    try:
        response = requests.get(f"{base_url}/random", headers={'Accept': 'application/json'})
        response.raise_for_status()
        data = response.json()
        print(f"Success! Fact: {data.get('text', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Test 2: Today's fact in English
    print("2. Test: Today's fact in English")
    try:
        response = requests.get(f"{base_url}/today", headers={'Accept': 'application/json'})
        response.raise_for_status()
        data = response.json()
        print(f"Success! Today's fact: {data.get('text', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Test 3: Check response structure
    print("3. Test: Response structure")
    try:
        response = requests.get(f"{base_url}/random", headers={'Accept': 'application/json'})
        response.raise_for_status()
        data = response.json()
        print(f"Response structure:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 