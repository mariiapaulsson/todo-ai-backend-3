import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Ladda miljövariabler från .env om du kör lokalt
load_dotenv()

# Initiera Flask och OpenAI-klient
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "API är live!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    # Kontrollera att alla fält finns
    if not all(k in data for k in ("query", "target_group", "location", "date")):
        return jsonify({"error": "Saknar ett eller flera fält"}), 400

    # Skapa prompt till ChatGPT
    prompt = (
        f"Vad händer i {data['location']} för målgruppen {data['target_group']} "
        f"den {data['date']}? Aktivitetssökning: {data['query']}."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam AI som ger tips på evenemang."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
