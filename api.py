from flask import Flask, request, jsonify
from flask_cors import CORS
from app import process

app = Flask(__name__)

# izinkan frontend localhost
CORS(app, resources={r"/query": {"origins": "*"}})

@app.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Question tidak ditemukan"}), 400

        result = process(data["question"])

        return jsonify({"result": result})

    except Exception as e:
        print("ERROR:", str(e))   # tampil di terminal backend
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)