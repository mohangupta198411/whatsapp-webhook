from flask import Flask, request
import requests
import json

app = Flask(__name__)

VERIFY_TOKEN = "adonnet123"  # Same as in Meta Webhook settings
MAKE_WEBHOOK_URL = "https://hook.us2.make.com/voq8kopsks8s9pwhwc1shtpn81ykxbul"  # Replace with your Make URL

@app.route('/', methods=['GET'])
def home():
    return 'Webhook is live 🎉'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verify token handshake
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403

    if request.method == 'POST':
        data = request.json
        print("🔔 Incoming Webhook Event:")
        print(json.dumps(data, indent=2))

        # Forward to Make webhook
        try:
            response = requests.post(MAKE_WEBHOOK_URL, json=data)
            print(f"✅ Forwarded to Make: {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to forward to Make: {str(e)}")

        return "EVENT_RECEIVED", 200

    return "Unsupported method", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
