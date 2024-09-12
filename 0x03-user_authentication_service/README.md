# 0x03 User Authentication 

## Description
This project is about user authentication. It is a simple user authentication service that is able to register, login and logout users. It is built using Flask, a micro web framework written in Python.

## Files
- `app.py`: The main file that contains the Flask app.
- `auth.py`: Contains the authentication logic.
- `db.py`: Contains the database logic.
- `user.py`: Contains the user logic.
- `main.py`: Contains the tests for the app.

## Usage
To run the app, execute the following command:
```
python3 app.py
```

To run the tests, execute the following command:
```
python3 main.py
```

## Endpoints
- `POST /users`: Register a new user.
- `POST /sessions`: Login a user.
- `DELETE /sessions`: Logout a user.
- `GET /profile`: Get the user profile.
- `GET /reset_password`: Reset the user password.
- `POST /reset_password`: Update the user password.

## Authors
- [Idaewor Favour](idaeworfavour1@gmail.com)


