#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def get_index():
    """Get index
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def user():
    """This provide route to users
    """
    if request.method == "POST":
        if request.is_json:
            data = request.get_json
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400

        try:
            user = AUTH.register_user(email, password)
            return jsonify({"email": user.email, "message":
                            "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
