import pandas as pd
from mf_model import MfModelOption, MFSentimentAnalyzer
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/v1', methods=['GET'])
def home():
    resp = {
        "message": "All service working normally.",
        "apiVersion": "v1.0.0" 
    }
    
    return jsonify(resp)

@app.route('/api/v1/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if 'reviews' not in data:
        return jsonify({'error': 'No reviews provided'}), 400
    
    if data.get("model") not in ['MFNb', 'MFSvc']:
        return jsonify({'error': 'No model found.'}), 400
    
    df = pd.DataFrame(data['reviews'])
    model_option = MfModelOption[data.get('model', 'MFNb')]
    
    mfModel = MFSentimentAnalyzer(df, model_option)
    result = mfModel.Analyze()
    resp = {
        "status": "success",
        "data": {
            "sentiment": result.to_dict(orient='records')
        }
    }
    
    return jsonify(resp)

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal Server Error, please try again later."
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
