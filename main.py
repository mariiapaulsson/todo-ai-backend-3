import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Initiera OpenAI-klient med API-nyckel från Render-miljö
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "API är live!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not all(k in data for k in ("query", "target_group", "location", "date")):
        return jsonify({"error": "Saknar ett eller flera fält"}), 400

    prompt = (
        f"Vad händer i {data['location']} för målgruppen {data['target_group']} "
        f"den {data['date']}? Aktivitetssökning: {data['query']}."
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
