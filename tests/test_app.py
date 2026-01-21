"""
Unit tests for Wine Cultivar Prediction System
Author: Eneasato David - 23CG034068

Run with: pytest tests/test_app.py
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test homepage loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Wine Cultivar' in response.data


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'model_loaded' in data


def test_model_info_endpoint(client):
    """Test model info endpoint"""
    response = client.get('/model-info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'model_info' in data
    assert data['model_info']['algorithm'] == 'Random Forest Classifier'


def test_prediction_valid_input(client):
    """Test prediction with valid input"""
    payload = {
        'alcohol': 13.5,
        'malic_acid': 2.0,
        'ash': 2.3,
        'magnesium': 110.0,
        'flavanoids': 2.5,
        'proline': 1000.0
    }
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'prediction' in data
    assert 'cultivar_name' in data
    assert 'confidence' in data
    assert 'probabilities' in data


def test_prediction_missing_feature(client):
    """Test prediction with missing feature"""
    payload = {
        'alcohol': 13.5,
        'malic_acid': 2.0,
        'ash': 2.3,
        'magnesium': 110.0,
        'flavanoids': 2.5
        # Missing proline
    }
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_prediction_invalid_value(client):
    """Test prediction with invalid value"""
    payload = {
        'alcohol': 'not_a_number',
        'malic_acid': 2.0,
        'ash': 2.3,
        'magnesium': 110.0,
        'flavanoids': 2.5,
        'proline': 1000.0
    }
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_prediction_empty_request(client):
    """Test prediction with empty request"""
    response = client.post(
        '/predict',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
