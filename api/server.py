from flask import Flask, render_template, request, jsonify, abort, render_template
from api.utility import struct_msg
from config import api_configuration

app = Flask(__name__,template_folder="../templates")
api_config = api_configuration()

@app.errorhandler(400)
def error_400(error):
    """
    handle 400 error
    Args:
        error: the flask error
    Returns:
        400 JSON error
    """
    return jsonify(
        struct_msg(status="error", msg=error.description)
    ), 400

@app.errorhandler(404)
def error_404(error):
    """
    handle 404 error
    Args:
        error: Authentication Failed
    Returns:
        404 JSON error
    """
    return jsonify(
        struct_msg(status="error", msg=error.description)
    ), 404

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
