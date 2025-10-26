"""
Basic API tests for Toxicity Assessment RAG System
Run with: pytest test_api.py -v
"""

import pytest
import requests
from time import sleep

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    print("✅ Root endpoint working")

def test_load_papers():
    """Test loading papers from PubMed"""
    payload = {
        "query": "parabens cosmetics toxicity",
        "max_results": 5
    }
    response = requests.post(f"{BASE_URL}/load-papers", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "papers_loaded" in data
    assert "average_quality_score" in data
    print(f"✅ Loaded {data['papers_loaded']} papers")
    
    # Wait a bit for processing
    sleep(2)

def test_stats():
    """Test getting database stats"""
    response = requests.get(f"{BASE_URL}/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_papers" in data
    assert "average_quality_score" in data
    print(f"✅ Database has {data['total_papers']} papers")

def test_assess():
    """Test toxicity assessment"""
    payload = {
        "substance": "parabens",
        "product_type": "cosmetics",
        "usage_frequency": "daily",
        "min_quality_score": 30,
        "max_papers": 3
    }
    response = requests.post(f"{BASE_URL}/assess", json=payload)
    
    if response.status_code == 404:
        print("⚠️  No papers found - load papers first")
        return
    
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert "confidence" in data
    assert "assessment" in data
    print(f"✅ Assessment complete: {data['risk_level']}")

def test_get_papers():
    """Test listing papers"""
    response = requests.get(f"{BASE_URL}/papers?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "papers" in data
    print(f"✅ Retrieved {len(data['papers'])} papers")

if __name__ == "__main__":
    print("Running API tests...")
    print("Make sure server is running: uvicorn main:app --reload")
    print("-" * 50)
    
    test_root_endpoint()
    test_load_papers()
    test_stats()
    test_assess()
    test_get_papers()
    
    print("-" * 50)
    print("✅ All tests passed!")
