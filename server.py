
from flask import Flask, request, jsonify
from model import answer_question  # your function that answers questions

app = Flask(__name__)

@app.route("/")
def index():
    return "RAG Gemini API is up!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing question"}), 400

    try:
        answer = answer_question(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Cloud Run will set PORT; default to 5002 locally
    import os
    port = int(os.getenv("PORT", 5002))
    app.run(host="0.0.0.0", port=port)

