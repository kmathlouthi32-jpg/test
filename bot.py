from flask import Flask, request
import requests

TOKEN = "7642185587:AAHypPZPZEQ8B7cgkqzl1SPuiPmThKjespo"  # 🔹 Replace with your token
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive! ✅"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "👋 Hello! I'm online 24/7 thanks to Render!")
        else:
            send_message(chat_id, f"You said: {text}")

    return "ok", 200


def send_message(chat_id, text):
    requests.post(API_URL + "sendMessage", json={"chat_id": chat_id, "text": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
