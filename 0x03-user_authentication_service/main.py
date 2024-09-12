#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test regiter user
    """
    url = "http://127.0.0.1:5000/users"
    data = {
        "email": email,
        "password": password
    }
    res = requests.post(url, data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test Login endpoint
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    res = requests.post(url, data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test Login endpoint
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    res = requests.post(url, data)
    assert res.status_code == 200
    assert res.json() == {"email": f"{email}", "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test Profile is not login
    """
    url = "http://127.0.0.1:5000/profile"
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test Profile is login
    """
    url = "http://127.0.0.1:5000/profile"
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """Test Profile is logout
    """
    url = "http://127.0.0.1:5000/sessions"
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.status_code != 403


def reset_password_token(email: str) -> str:
    """Test reset pasword token
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email
    }
    res = requests.post(url, data)
    assert res.status_code == 200
    data = res.json()
    return data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put(url, data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
