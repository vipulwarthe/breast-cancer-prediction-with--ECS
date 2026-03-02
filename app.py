import pickle
import numpy as np
from flask import Flask, request, jsonify

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load scaler
with open('scaler.pkl', 'rb') as f:
    sc = pickle.load(f)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({"error": "Missing 'features' key"}), 400

        features = data["features"]

        if len(features) != 30:
            return jsonify({"error": "Exactly 30 features required"}), 400

        unseen_data = np.array([features]).astype(np.float64)

        # ✅ Apply scaling
        unseen_data_scaled = sc.transform(unseen_data)

        prediction = model.predict(unseen_data_scaled)[0]

        return jsonify({
            "prediction": int(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

































