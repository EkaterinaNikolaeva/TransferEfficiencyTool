from flask import Flask, request, send_from_directory, jsonify, Response
import os
import argparse
from werkzeug.http import parse_range_header

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


def get_range(range_header, file_size):
    range_parsed = parse_range_header(range_header)
    if not range_parsed:
        raise RequestException(416, "Invalid Range header")
    start, end = range_parsed.ranges[0]
    if start is None:
        start = 0
    if end is None:
        end = file_size - 1
    if start < 0 or end >= file_size or start > end:
        raise RequestException(416, "Bad range")
    return start, end


@app.route("/<path:filename>", methods=["GET"])
def download_file(filename):
    range_header = request.headers.get("Range", None)
    if not range_header:
        return send_from_directory(STORAGE, filename, as_attachment=True)
    file = os.path.join(STORAGE, filename)
    file_size = os.path.getsize(file)
    start, end = get_range(request.headers["Range"], file_size)

    def generate():
        with open(file, "rb") as f:
            f.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = f.read(min(8192, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk

    response = Response(generate(), status=206, mimetype="application/octet-stream")
    response.headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response.headers["Accept-Ranges"] = "bytes"
    return response


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
