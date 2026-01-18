from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load model artifacts
MODEL_PATH = os.path.join('artifacts', 'flight_delay_model.pkl')
PREPROCESSOR_PATH = os.path.join('artifacts', 'flight_delay_preprocess.pkl')
FEATURE_STORE_PATH = os.path.join('artifacts', 'feature_store.csv')

print("Loading model and preprocessor...")
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
feature_store = pd.read_csv(FEATURE_STORE_PATH)
print("Load complete.")

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    carriers = sorted(feature_store['carrier'].unique().tolist())
    airports = sorted(feature_store['airport'].unique().tolist())
    return jsonify({
        'carriers': carriers,
        'airports': airports
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        carrier = data.get('carrier')
        airport = data.get('airport')
        month = int(data.get('month'))
        
        # Calculate derived features
        month_sin = np.sin(2 * np.pi * month / 12)
        month_cos = np.cos(2 * np.pi * month / 12)
        
        lookup = feature_store[(feature_store['carrier'] == carrier) & (feature_store['airport'] == airport)]
        
        if lookup.empty:
            # Fallback to global averages if no specific carrier/airport data found
            log_arr_flights = feature_store['log_arr_flights'].mean()
            delay_rate_lag1 = feature_store['delay_rate_lag1'].mean()
            delay_rate_lag2 = feature_store['delay_rate_lag2'].mean()
            delay_rate_lag3 = feature_store['delay_rate_lag3'].mean()
            log_arr_flights_lag1 = feature_store['log_arr_flights_lag1'].mean()
        else:
            month_match = lookup[lookup['month'] == month]
            if not month_match.empty:
                row = month_match.mean(numeric_only=True)
                log_arr_flights = row['log_arr_flights']
                delay_rate_lag1 = row['delay_rate_lag1']
                delay_rate_lag2 = row['delay_rate_lag2']
                delay_rate_lag3 = row['delay_rate_lag3']
                log_arr_flights_lag1 = row['log_arr_flights_lag1']
            else:
                latest = lookup.sort_values(['year', 'month'], ascending=False).iloc[0]
                log_arr_flights = latest['log_arr_flights']
                delay_rate_lag1 = latest['delay_rate_lag1']
                delay_rate_lag2 = latest['delay_rate_lag2']
                delay_rate_lag3 = latest['delay_rate_lag3']
                log_arr_flights_lag1 = latest['log_arr_flights_lag1']
            
        # Defaults for hidden technical features
        arr_cancelled = 0.0
        arr_diverted = 0.0

        # Prepare input DataFrame for preprocessor
        input_data = pd.DataFrame([{
            'carrier': carrier,
            'airport': airport,
            'log_arr_flights': log_arr_flights,
            'arr_cancelled': arr_cancelled,
            'arr_diverted': arr_diverted,
            'month_sin': month_sin,
            'month_cos': month_cos,
            'delay_rate_lag1': delay_rate_lag1,
            'delay_rate_lag2': delay_rate_lag2,
            'delay_rate_lag3': delay_rate_lag3,
            'log_arr_flights_lag1': log_arr_flights_lag1
        }])
        
        # Preprocess and predict
        X_processed = preprocessor.transform(input_data)
        prediction = model.predict(X_processed)
        
        # LightGBM Regressor returns an array
        prediction_val = float(prediction[0])
        
        return jsonify({
            'prediction': prediction_val,
            'log_arr_flights_used': float(log_arr_flights), # Returning for transparency
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5005)
