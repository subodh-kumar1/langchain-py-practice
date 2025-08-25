from http import HTTPStatus

from flask import Flask, request, jsonify

from generate_and_save_embedding import save_embedding_using_index
from git_clone import clone_code
from load_chunks import load_chunks
from src.const import INDEX_NAME

from chat import query_model


app = Flask(__name__)


@app.route("/embed", methods=["POST"])
def embed():
    payload = request.get_json()
    try:
        # Step 1 :  Clone git repo to local dir
        clone_code(payload["repo_url"])
        # Step 2 :  Load code from local dir
        chunks = load_chunks()
        # Step 3 :  Convert the code in embedding and save in DB along with metadata
        response = save_embedding_using_index(payload.get("db_name", INDEX_NAME), chunks)
        return jsonify({"success": True, "response": response}), HTTPStatus.OK
    except Exception as exp:
        return jsonify({"success": False, "response": exp}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json()
    try:
        # Step 4 :  Query model
        answer, source_docs = query_model(payload["question"], payload.get("db_name", INDEX_NAME))
        return jsonify({"success": True, "response": answer, "source_documents": list(source_docs)}), HTTPStatus.OK
    except Exception as exp:
        return jsonify({"success": False, "response": str(exp)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/test", methods=["GET"])
def test():
    return "test"

if __name__ == "__main__":
    app.run(debug=True)
