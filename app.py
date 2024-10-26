# app.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pyotp
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Get SECRET from environment variables
SECRET = os.getenv('SECRET_KEY')
if not SECRET:
    raise ValueError("SECRET_KEY environment variable is not set")

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/code')
def get_code():
    totp = pyotp.TOTP(SECRET)
    current_code = totp.now()
    remaining_time = 30 - int(time.time()) % 30
    
    return jsonify({
        'code': current_code,
        'remainingSeconds': remaining_time
    })

# Vercel requires this
app.debug = False

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)