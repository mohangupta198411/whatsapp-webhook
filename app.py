from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Your WhatsApp Webhook verify token
VERIFY_TOKEN = 'adonnet123'

# Your Make.com webhook URL (replace with actual Make endpoint)
MAKE_WEBHOOK_URL = 'https://hook.us2.make.com/voq8kopsks8s9pwhwc1shtpn81ykxbul'

@app.route('/', methods=['GET'])
def health_check():
    return "🚀 WhatsApp Webhook is running", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification logic
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified")
            return challenge, 200
        else:
            print("❌ Webhook verification failed")
            return "Verification failed", 403

    elif request.method == 'POST':
        try:
            data = request.get_json()
            print("📨 Incoming WhatsApp message:")
            print(json.dumps(data, indent=2))

            # Forward to Make
            response = requests.post(MAKE_WEBHOOK_URL, json=data)
            print(f"➡️ Forwarded to Make - Status code: {response.status_code}")

            return "EVENT_RECEIVED", 200

        except Exception as e:
            print(f"❌ Error processing webhook: {e}")
            return "ERROR", 500

if __name__ == '__main__':
    # Flask will listen on all IPs, port 10000 (as required by Render)
    app.run(debug=True, host='0.0.0.0', port=10000)
