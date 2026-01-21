# Wine Cultivar Prediction System - Deployment Guide

**Author:** Eneasato David  
**Matric No:** 23CG034068

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Trained model file (`model/wine_cultivar_model.pkl`)
- ✅ All project files in correct structure
- ✅ GitHub account
- ✅ Deployment platform account (Render/PythonAnywhere/etc.)

---

## 🚀 Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

#### Step 1: Prepare GitHub Repository

```bash
# Navigate to project directory
cd "C:\Users\user\Documents\Covenant University\300Lvl Alpha\Newer\300l alpha 25-26\COS331 - Artificial Intelligence (AI)\Projects\WineCultivar_Project_Eneasato_David_23CG034068"

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Wine Cultivar Prediction System"

# Create GitHub repository (via GitHub website), then:
git remote add origin https://github.com/YOUR_USERNAME/WineCultivar_Project_23CG034068.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy on Render

1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your repository
5. Configure:
   - **Name**: wine-cultivar-predictor
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment
8. Copy your live URL (e.g., https://wine-cultivar-predictor.onrender.com)

#### Step 3: Test Deployment

```bash
# Test the health endpoint
curl https://your-app-name.onrender.com/health

# Should return: {"status": "healthy", "model_loaded": true, ...}
```

---

### Option 2: PythonAnywhere.com

#### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Verify email

#### Step 2: Upload Files
1. Go to "Files" tab
2. Create directory: `WineCultivar_Project`
3. Upload all project files:
   - `app.py`
   - `requirements.txt`
   - Upload `model/` folder with model file
   - Upload `templates/` folder
   - Upload `static/` folder

#### Step 3: Install Dependencies
1. Go to "Consoles" tab
2. Start a Bash console
3. Run:
```bash
cd WineCultivar_Project
pip3.10 install --user -r requirements.txt
```

#### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Select "Flask"
4. Python version: 3.10
5. Edit WSGI configuration file:

```python
import sys
import os

# Add your project directory
project_home = '/home/YOUR_USERNAME/WineCultivar_Project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

6. Set working directory: `/home/YOUR_USERNAME/WineCultivar_Project`
7. Click "Reload" button
8. Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

### Option 3: Streamlit Cloud (Alternative)

If you prefer Streamlit instead of Flask:

#### Step 1: Convert to Streamlit

Create `streamlit_app.py`:

```python
import streamlit as st
import joblib
import numpy as np

# Load model
model_package = joblib.load('model/wine_cultivar_model.pkl')

st.title('🍷 Wine Cultivar Prediction System')

# Input fields
alcohol = st.number_input('Alcohol', value=13.5)
malic_acid = st.number_input('Malic Acid', value=2.0)
ash = st.number_input('Ash', value=2.3)
magnesium = st.number_input('Magnesium', value=110.0)
flavanoids = st.number_input('Flavanoids', value=2.5)
proline = st.number_input('Proline', value=1000.0)

if st.button('Predict'):
    # Make prediction
    features = [alcohol, malic_acid, ash, magnesium, flavanoids, proline]
    scaled = model_package['scaler'].transform([features])
    prediction = model_package['model'].predict(scaled)[0]
    
    st.success(f'Predicted Cultivar: {model_package["target_names"][prediction]}')
```

#### Step 2: Deploy

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Deploy!

---

## 🧪 Post-Deployment Testing

### Test Checklist

1. **Homepage loads** ✓
   - Navigate to your deployed URL
   - Check if the form displays correctly

2. **Health endpoint works** ✓
   ```bash
   curl https://your-app-url.com/health
   ```

3. **Model info endpoint works** ✓
   ```bash
   curl https://your-app-url.com/model-info
   ```

4. **Prediction works** ✓
   - Fill in the form with sample data
   - Submit and verify prediction appears

5. **Mobile responsive** ✓
   - Open on mobile device
   - Check layout and functionality

---

## 📝 Update Submission File

After successful deployment:

1. Open `WineCultivar_hosted_webGUI_link.txt`
2. Update with your actual URLs:
   - Live application URL
   - GitHub repository URL
3. Save the file

---

## 🔧 Troubleshooting

### Issue: Model file not found

**Solution:**
- Ensure `model/wine_cultivar_model.pkl` exists
- Run the Jupyter notebook to generate it
- Verify it's included in your git repository

### Issue: Dependencies not installing

**Solution:**
```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### Issue: Render deployment fails

**Solution:**
- Check build logs for errors
- Ensure Python version is 3.8+
- Verify all file paths are relative, not absolute

### Issue: Port binding error

**Solution:**
- Ensure app.py uses: `port = int(os.environ.get('PORT', 5000))`
- Don't hardcode port numbers

---

## 📊 Monitoring

### Check Application Health

```bash
# Health check
curl https://your-app-url.com/health

# Model information
curl https://your-app-url.com/model-info
```

### View Logs

**Render:**
- Go to your service dashboard
- Click "Logs" tab

**PythonAnywhere:**
- Go to "Web" tab
- Click "Log files" section

---

## 🎯 Final Submission Steps

1. ✅ Train model (run notebook)
2. ✅ Test locally (`python app.py`)
3. ✅ Push to GitHub
4. ✅ Deploy to chosen platform
5. ✅ Test deployment
6. ✅ Update `WineCultivar_hosted_webGUI_link.txt`
7. ✅ Create project ZIP file
8. ✅ Submit to Scorac.com

---

## 📦 Create Submission Package

```bash
# Navigate to parent directory
cd ..

# Create ZIP file (Windows PowerShell)
Compress-Archive -Path "WineCultivar_Project_Eneasato_David_23CG034068" -DestinationPath "WineCultivar_Project_Eneasato_David_23CG034068.zip"

# Verify contents
# Should include:
# - app.py
# - requirements.txt
# - WineCultivar_hosted_webGUI_link.txt
# - model/ (with model_building.ipynb and wine_cultivar_model.pkl)
# - static/ (with style.css)
# - templates/ (with index.html)
```

---

## 🎓 Submission Deadline

**Thursday, January 21, 2026 - 11:59 PM**

Submit to: Scorac.com

---

## 📞 Support

For deployment issues:
- Render: https://render.com/docs
- PythonAnywhere: https://help.pythonanywhere.com/
- Flask: https://flask.palletsprojects.com/

---

**Good luck with your deployment! 🚀**

---

**Eneasato David | 23CG034068 | Covenant University**
