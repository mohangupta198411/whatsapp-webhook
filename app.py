from flask import Flask, request
import json
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'adonnet123'
MAKE_WEBHOOK_URL = 'https://hook.us2.make.com/voq8kopsks8s9pwhwc1shtpn81ykxbul'  # 🔁 Replace this with your actual Make URL

@app.route('/', methods=['GET'])
def home():
    return 'WhatsApp Webhook is Running ✅'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('✅ Webhook Verified')
            return challenge, 200
        else:
            return 'Verification failed', 403

    elif request.method == 'POST':
        data = request.get_json()
        print('📨 Incoming WhatsApp Webhook:')
        print(json.dumps(data, indent=2))

        # Forward payload to Make
        try:
            response = requests.post(MAKE_WEBHOOK_URL, json=data)
            print(f'🔁 Forwarded to Make | Status: {response.status_code}')
        except Exception as e:
            print(f'❌ Error forwarding to Make: {str(e)}')

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(debug=True, port=10000, host='0.0.0.0')
