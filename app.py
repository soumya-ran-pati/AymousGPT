from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Store chat history (basic version)
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    messages.append({"role": "user", "content": user_input})

    # Limit memory
    if len(messages) > 10:
        messages[:] = [messages[0]] + messages[-9:]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)