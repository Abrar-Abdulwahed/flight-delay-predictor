# Flight Delay Predictor

A modern, high-performance web application designed to predict flight delay probabilities using advanced machine learning. The project features a robust Flask-based inference API and a sleek, interactive glassmorphic UI.

---

## Overview

This predictor leverages a **LightGBM** model trained on historical flight data to estimate the likelihood of arrival delays. By analyzing the carrier, airport, and time of year (month), the system provides real-time risk assessments to help travelers and logistics planners anticipate potential disruptions.

## Tech Stack

### Backend (MLOps & API)
- **Framework:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Machine Learning:** LightGBM, Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Inference:** Joblib (Model & Preprocessor loading)
- **Cross-Origin Support:** Flask-CORS

### Frontend (User Interface)
- **Language:** Vanilla JavaScript (ES6+)
- **Styling:** Vanilla CSS3 (Custom properties, Flexbox/Grid, Glassmorphism)
- **Typography:** [Outfit](https://fonts.google.com/specimen/Outfit) via Google Fonts
- **Aesthetics:** Dark mode, micro-animations, and dynamic risk meters.

---

## Key Features

- **Real-time Prediction:** Sub-second inference powered by professional ML pipelines.
- **Dynamic Data Discovery:** Automatically fetches available carriers and airports from the feature store.
- **Interactive UI:**
  - **Radar Analysis:** Visual "scanning" animation during prediction.
  - **Risk Meter:** Color-coded severity indicators (Low/Medium/High).
  - **Responsive Design:** Optimized for both desktop and mobile viewing.
- **Fallback Logic:** Intelligent handling for carrier/airport combinations not explicitly in the training set using global averages.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.9+
- Pip (Python Package Manager)

### 2. Backend Setup
1. Navigate to the project directory.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Running the Application
1. **Start the API Server:**
   ```bash
   python app.py
   ```
   The backend will start on `http://127.0.0.1:5005`.

2. **Launch the Interface:**
   Simply open `index.html` in any modern web browser.

---

## Project Structure

```text
API_MLOPS/
├── artifacts/                # Trained models and feature data
│   ├── flight_delay_model.pkl
│   ├── flight_delay_preprocess.pkl
│   └── feature_store.csv
├── app.py                    # Flask API & logic
├── index.html                # Frontend structure
├── style.css                 # Premium styling
├── script.js                 # API interaction & UI logic
├── requirements.txt          # Python dependencies
└── .gitignore                # Comprehensive ignore rules
```

## License
This project is for educational purposes as part of the AI-Approach-Club.
