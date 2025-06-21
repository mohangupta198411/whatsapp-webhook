from flask import Flask, request
import os
import json

app = Flask(__name__)

VERIFY_TOKEN = "adonnet123"  # Same token used in Meta webhook settings

@app.route("/", methods=["GET"])
def home():
    return "Webhook is Live ✅"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verification challenge
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified!")
            return challenge, 200
        else:
            print("❌ Webhook verification failed.")
            return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        print("📨 Received webhook event:")
        print(json.dumps(data, indent=2))
        return "EVENT_RECEIVED", 200

    return "Method not allowed", 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
