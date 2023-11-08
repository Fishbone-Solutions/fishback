from flask_cors import CORS
from flask import Flask, jsonify,request
from app.emails_alerts import send_alerts
from app.configs import email_list


app = Flask(__name__)
CORS(app)


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["JWT_ALGORITHM"] = "HS256"

app.config["JWT_ALGORITHM"] = "HS256"
app.config["SECRET_KEY"] = "IUGYGFYR456547E47636RDNGTXSDR"


@app.route("/login", methods=["POST"])
def login():
    print("hello")


@app.errorhandler(404)
def error_404(e):
    return '<h1>Bad Request</h1>', 404


@app.route('/stack_addition', methods=['POST'])
def handle_addtion():
    data = request.json
    send_alerts(reciepents=email_list, message_content=data)
    response = {
        "req_id": 90
    }
    return jsonify(response)

