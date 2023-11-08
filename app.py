from flask import Flask, request,jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/stack_addition', methods=['POST'])
def data():
    rq = request.get_json()
    return jsonify(rq)

if __name__ == '__main__':
    app.run()