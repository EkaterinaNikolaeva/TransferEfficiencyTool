from flask import Flask, request, send_from_directory, jsonify
import os
import argparse

app = Flask(__name__)

STORAGE = ""


class RequestException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(RequestException)
def handle_exception(err):
    response = {
        "message": err.message,
    }
    return jsonify(response), err.status_code


@app.route("/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(STORAGE, filename, as_attachment=True)


@app.route("/<path:filename>", methods=["HEAD"])
def check_file_exists(filename):
    file_path = os.path.join(STORAGE, filename)
    if not os.path.isfile(file_path):
        raise RequestException(404, "File does not exist")
    return "Ok", 200


@app.route("/<path:filename>", methods=["PUT"])
def upload_file(filename):
    file_path = os.path.join(STORAGE, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            f.write(request.data)
        return "Ok", 200
    except Exception as e:
        raise RequestException(500, "Error when try to save file: {}".format(e))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--storage", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    STORAGE = args.storage
    os.makedirs(STORAGE, exist_ok=True)
    app.run(host="127.0.0.1", port=8000)
