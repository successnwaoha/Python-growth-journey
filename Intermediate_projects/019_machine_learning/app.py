from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os # Add this import at the top

app = Flask(__name__)

# 1. Load the "brain" we trained earlier
model = joblib.load('titanic_model.pkl')

REQUIRED_KEYS = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get the JSON data FIRST
        data = request.get_json()
        
        # 2. NOW check if any keys are missing
        missing = [key for key in REQUIRED_KEYS if key not in data]
        if missing:
            return jsonify({
                'status': 'error',
                'message': f'Missing fields: {", ".join(missing)}'
            }), 400 

        # 3. Convert JSON to a DataFrame
        input_df = pd.DataFrame([data])
        
        # 4. Make a prediction & get probability
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        result = "Survived" if prediction == 1 else "Did not survive"
        
        return jsonify({
            'prediction': result,
            'confidence': f"{probability:.2%}",
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'fail'})

if __name__ == '__main__':
    # Use the port assigned by the cloud, or 5001 if running locally
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)