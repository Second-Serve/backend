from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  

@app.route('/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from the Python backend!"}
    return jsonify(data)

@app.route('/data', methods=['POST'])
def post_data():
    data = request.json
    response = {"received": data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)