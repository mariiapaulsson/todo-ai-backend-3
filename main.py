import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initiera OpenAI-klient
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "API är live!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    # Validera fält
    if not all(k in data for k in ("query", "target_group", "location", "dates")):
        return jsonify({"error": "Saknar ett eller flera fält"}), 400

    query = data["query"]
    target_group = data["target_group"]
    location = data["location"]
    dates = data["dates"]
    free_only = data.get("free", False)

    # Bygg prompt med flera datum
    date_str = ", ".join(dates)
    free_text = " Endast gratis aktiviteter." if free_only else ""

    prompt = (
        f"Vad händer i {location} för målgruppen {target_group} "
        f"på följande datum: {date_str}? Aktivitetssökning: {query}.{free_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam AI som föreslår lokala aktiviteter och evenemang."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

@app.route("/ask-chat", methods=["POST"])
def ask_chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Meddelande saknas"}), 400

    prompt = data["message"]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                 {"role": "system", "content": "Du är en hjälpsam AI som föreslår lokala aktiviteter och evenemang."},
)
                },
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
