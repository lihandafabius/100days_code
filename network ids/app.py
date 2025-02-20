import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)
model = joblib.load('stacked_meta_model.pkl')

# Dictionary to map service and flag categories to numerical values
service_mapping = {
    'http': 0,
    'private': 1,
    'ftp_data': 2,
    # Add more mappings as needed
}

flag_mapping = {
    'SF': 0,
    'S0': 1,
    'REJ': 2,
    # Add more mappings as needed
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        service = request.form['service']
        flag = request.form['flag']
        src_bytes = float(request.form['src_bytes'])
        dst_bytes = float(request.form['dst_bytes'])
        count = float(request.form['count'])

        # Map categorical values to numerical
        service_encoded = service_mapping.get(service, -1)  # Default to -1 if service not found
        flag_encoded = flag_mapping.get(flag, -1)          # Default to -1 if flag not found

        # Ensure valid mapping for service and flag
        if service_encoded == -1 or flag_encoded == -1:
            return render_template('index.html', output="Error: Invalid service or flag")

        # Construct the feature array with 5 elements
        features = [service_encoded, flag_encoded, src_bytes, dst_bytes, count]

        # Prepare the final feature array
        final_features = [np.array(features)]

        # Debugging print
        print(f"Final features: {final_features}")

        # Make prediction
        prediction = model.predict(final_features)

        # Map prediction result to attack types
        if prediction == 0:
            output = 'Normal'
        elif prediction == 1:
            output = 'DOS'
        elif prediction == 2:
            output = 'PROBE'
        elif prediction == 3:
            output = 'R2L'
        else:
            output = 'U2R'

        return render_template('index.html', output=output)

    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('index.html', output="Error: Unable to process the input")

@app.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json(force=True)
        predict = model.predict([np.array(list(data.values()))])

        if predict == 0:
            output = 'Normal'
        elif predict == 1:
            output = 'DOS'
        elif predict == 2:
            output = 'PROBE'
        elif predict == 3:
            output = 'R2L'
        else:
            output = 'U2R'

        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
