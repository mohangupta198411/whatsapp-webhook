from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = 'adonnet123'
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge')
        return 'Invalid token', 403

    if request.method == 'POST':
        data = request.json
        print("Received webhook event:", data)
        return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
