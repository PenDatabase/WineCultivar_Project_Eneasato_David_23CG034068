"""
Quick Start Script for Wine Cultivar Prediction System
Author: Eneasato David - 23CG034068

This script helps you quickly set up and run the application.
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible!")
    return True


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies!")
        return False


def check_model_exists():
    """Check if trained model exists"""
    print_header("Checking for Trained Model")
    
    model_path = Path("model/wine_cultivar_model.pkl")
    
    if model_path.exists():
        print(f"✅ Model found at: {model_path}")
        print(f"   Size: {model_path.stat().st_size / 1024:.2f} KB")
        return True
    else:
        print("⚠️  Model file not found!")
        print("\nYou need to train the model first:")
        print("1. Open Jupyter Notebook: jupyter notebook")
        print("2. Navigate to: model/model_building.ipynb")
        print("3. Run all cells to train and save the model")
        print("\nOr run: jupyter nbconvert --to notebook --execute model/model_building.ipynb")
        return False


def run_app():
    """Run the Flask application"""
    print_header("Starting Flask Application")
    
    print("Starting server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped!")


def main():
    """Main execution flow"""
    print("\n🍷 Wine Cultivar Prediction System - Quick Start")
    print("Author: Eneasato David | Matric No: 23CG034068\n")
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install dependencies
    print("\nDo you want to install/update dependencies? (y/n): ", end="")
    if input().lower() == 'y':
        if not install_dependencies():
            return
    else:
        print("Skipping dependency installation...")
    
    # Step 3: Check for model
    if not check_model_exists():
        print("\n⚠️  Cannot start application without trained model!")
        return
    
    # Step 4: Run the application
    print("\nReady to start the application!")
    print("Start server? (y/n): ", end="")
    if input().lower() == 'y':
        run_app()
    else:
        print("\nSetup complete! Run 'python app.py' when ready.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
