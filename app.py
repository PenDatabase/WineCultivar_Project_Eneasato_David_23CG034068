"""
Wine Cultivar Origin Prediction System - Flask Web Application

Author: Eneasato David
Matric No: 23CG034068
Date: January 21, 2026

This Flask application provides a web interface for predicting wine cultivar
origin based on chemical properties using a trained Random Forest model.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Model configuration
MODEL_PATH = Path('model/wine_cultivar_model.pkl')
model_package = None


def load_model() -> Dict[str, Any]:
    """
    Load the trained model package from disk.
    
    Returns:
        Dict containing model, scaler, feature names, and metadata
    
    Raises:
        FileNotFoundError: If model file doesn't exist
        Exception: If model loading fails
    """
    global model_package
    
    if model_package is not None:
        return model_package
    
    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        logger.info(f"Loading model from {MODEL_PATH}")
        model_package = joblib.load(MODEL_PATH)
        
        # Validate model package structure
        required_keys = ['model', 'scaler', 'feature_names', 'target_names']
        if not all(key in model_package for key in required_keys):
            raise ValueError("Invalid model package structure")
        
        logger.info("Model loaded successfully")
        logger.info(f"Algorithm: {model_package['metadata']['algorithm']}")
        logger.info(f"Test Accuracy: {model_package['metadata']['test_accuracy']:.4f}")
        
        return model_package
    
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def validate_input(data: Dict[str, Any], feature_names: list) -> Tuple[bool, str]:
    """
    Validate user input data.
    
    Args:
        data: Dictionary containing feature values
        feature_names: List of expected feature names
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if all required features are present
    missing_features = [f for f in feature_names if f not in data]
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features)}"
    
    # Validate that all values are numeric
    for feature in feature_names:
        try:
            value = float(data[feature])
            if not np.isfinite(value):
                return False, f"Invalid value for {feature}: must be a finite number"
        except (ValueError, TypeError):
            return False, f"Invalid value for {feature}: must be a number"
    
    return True, ""


def predict_cultivar(input_features: Dict[str, float]) -> Dict[str, Any]:
    """
    Predict wine cultivar from input features.
    
    Args:
        input_features: Dictionary with feature names as keys and values as floats
    
    Returns:
        Dictionary containing prediction results
    
    Raises:
        ValueError: If input validation fails
    """
    # Load model if not already loaded
    package = load_model()
    
    # Validate input
    is_valid, error_msg = validate_input(input_features, package['feature_names'])
    if not is_valid:
        raise ValueError(error_msg)
    
    try:
        # Extract components
        model = package['model']
        scaler = package['scaler']
        feature_names = package['feature_names']
        target_names = package['target_names']
        
        # Prepare input array in correct feature order
        input_array = np.array([[float(input_features[f]) for f in feature_names]])
        
        # Scale and predict
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        
        # Prepare response
        result = {
            'success': True,
            'prediction': int(prediction),
            'cultivar_name': target_names[prediction],
            'confidence': float(probabilities[prediction]),
            'probabilities': {
                target_names[i]: float(prob) for i, prob in enumerate(probabilities)
            },
            'input_features': {f: float(input_features[f]) for f in feature_names}
        }
        
        logger.info(f"Prediction made: {result['cultivar_name']} (confidence: {result['confidence']:.2%})")
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise


@app.route('/')
def index():
    """Render the main page."""
    try:
        # Load model to get feature names and metadata
        package = load_model()
        
        return render_template(
            'index.html',
            features=package['feature_names'],
            algorithm=package['metadata']['algorithm'],
            accuracy=f"{package['metadata']['test_accuracy']*100:.2f}"
        )
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return render_template('error.html', error=str(e)), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get JSON data from request
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if not data:
            raise BadRequest("No input data provided")
        
        # Make prediction
        result = predict_cultivar(data)
        
        return jsonify(result), 200
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': 'validation_error'
        }), 400
    
    except Exception as e:
        logger.error(f"Prediction endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An internal error occurred. Please try again.',
            'error_type': 'server_error'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    try:
        package = load_model()
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'algorithm': package['metadata']['algorithm'],
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e)
        }), 500


@app.route('/model-info')
def model_info():
    """Endpoint to get model information and metadata."""
    try:
        package = load_model()
        metadata = package['metadata']
        
        return jsonify({
            'success': True,
            'model_info': {
                'algorithm': metadata['algorithm'],
                'features': package['feature_names'],
                'target_classes': package['target_names'],
                'performance': {
                    'test_accuracy': metadata['test_accuracy'],
                    'train_accuracy': metadata['train_accuracy'],
                    'precision': metadata['precision'],
                    'recall': metadata['recall'],
                    'f1_score': metadata['f1_score'],
                    'cv_mean_accuracy': metadata['cv_mean_accuracy']
                },
                'training_date': metadata['trained_on'],
                'author': metadata['author'],
                'matric_no': metadata['matric_no']
            }
        }), 200
    except Exception as e:
        logger.error(f"Model info endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'error_type': 'not_found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'error_type': 'server_error'
    }), 500


if __name__ == '__main__':
    # Production deployment should use a proper WSGI server (gunicorn, waitress)
    # This is for development/testing only
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
