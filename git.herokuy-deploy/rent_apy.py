from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pickle
import numpy as np
import logging
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    logging.info("a logging test")
    print("----------------------------------------------")
    print(request.json['data'])
    print("**********************************************")
    #json_ = request.json
    model_file_path = 'rent_price_predictor.pkl'        
    model = pickle.load(open(model_file_path, 'rb'))
    payload = request.json['data']

    query_df = pd.DataFrame([payload])
    query = query_df.values
    prediction = model.predict(query)
    return jsonify({'prediction': list(prediction)})

    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 5000)))
    #app.run(debug=False, host='0.0.0.0', port=5000)