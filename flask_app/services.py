from typing import Optional

import jwt
import requests

from app import app
from database.models import User, save_obj


def get_request_user(request):
    session_id = request.cookies.get("session_id", "no_session_id")
    return User.query.filter_by(session_id=session_id).first()


def request_is_authenticated(request):
    session_id = request.cookies.get("session_id", "")
    if session_id:
        return User.query.filter_by(session_id=session_id).count()
    return False


def user_login(form):
    password = jwt.encode({"password": form["password"]}, app.config["SECRET_KEY"], algorithm="HS256")
    user = User.query.filter_by(username=form["username"], password=password).first()

    if user:
        user.session_id = jwt.encode({"uid": user.id}, app.config["SECRET_KEY"], algorithm="HS256")
        save_obj(user)
        return True, user.session_id

    return False, ""


def user_register(form):
    username = form["username"]
    password1 = form["password1"]
    password2 = form["password2"]

    if password1 == password2:
        user = User.query.filter_by(username=username).first()

        if user:
            return False

        password = jwt.encode({"password": password1}, app.config["SECRET_KEY"], algorithm="HS256")
        user = User(username=username, password=password)
        save_obj(user)
        return True

    return False


def user_logout(request):
    user = get_request_user(request)
    user.session_id = None
    save_obj(user)


def _fastapi_request(route: str, method: str, json_data: Optional[dict]):
    if method == "get":
        response = requests.get(app.config["FASTAPI_URL"] + route)
    else:  # if method == "post"
        response = requests.post(app.config["FASTAPI_URL"] + route, json=json_data)

    return response.json()


def api_get_user_projects(user: User):
    fastapi_response = _fastapi_request("get_user_projects", "post", {"user_id": user.id})
    return fastapi_response
