from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ladda API-nyckeln från miljövariabel
openai.api_key = os.getenv("OPENAI_API_KEY")
print("API-nyckel laddad:", openai.api_key)


@app.route("/")
def home():
    return "API är live!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    target_group = data.get("target_group", "")
    location = data.get("location", "")
    date = data.get("date", "")

    prompt = f"Ge förslag på aktiviteter för målgruppen {target_group} i {location} den {date}, relaterade till '{query}'."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message["content"].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
