#!/usr/bin/env python3
"""Flask app
"""
from flask import abort, Flask, jsonify, request, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
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


@app.route("/sessions", methods=["POST"])
def login():
    """Login route
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

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            resp = jsonify({"email": email, "message": "logged in"})
            resp.set_cookie("session_id", session_id)
            return resp
        else:
            abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout route
    """
    if request.method == "DELETE":
        session_id = request.cookies.get('session_id')
        if session_id is None:
            abort(403)

        try:
            user = AUTH.get_user_from_session_id(session_id)
            AUTH.destroy_session(user.id)
            resp = redirect(url_for('index'))
            resp.delete_cookie('session_id')
            return resp
        except NoResultFound:
            abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Profile route
    """
    if request.method == "GET":
        session_id = request.cookies.get("session_id")
        if session_id is None:
            abort(403)

        try:
            user = AUTH.get_user_from_session_id(session_id)
            return jsonify({"email": f"{user.email}"}), 200
        except Exception as e:
            abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """route to reset password
    """
    if request.method == "POST":
        if request.is_json:
            data = request.get_json
        else:
            data = request.form

        email = data.get("email")
        if email is None:
            abort(403)

        try:
            tkn = AUTH.get_reset_password_token(email)
            return jsonify({"email": f"{email}", "reset_token": f"{tkn}"}), 200
        except ValueError:
            abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
