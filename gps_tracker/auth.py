import base64
import typing
import hashlib

import pymongo.errors

from gps_tracker.mongo import look_up_user


def decrypt_header(content: str) -> (str, str):
    if not content:
        return None, None

    content_bytes: bytes = content.encode(encoding="ascii")
    message_bytes: bytes = base64.b64decode(s=content_bytes)
    message: str = message_bytes.decode(encoding="ascii")

    if message.count(":") == 1:
        username, password = message.split(":")
        return username, password

    return None, None


# returns key
def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=bytes.fromhex(salt),
        iterations=123456
    ).hex()


def is_user_authenticated(headers: typing.Dict[str, str]) -> (str, bool, int):

    # check if header is supplied
    header = headers.get("Authorization", "")
    if not header:
        return "Authorization header missing", False, 400

    if header[:5] != "Basic":
        return "Use basic authorisation method", False, 400

    username, password = decrypt_header(content=header[6:])
    if not username or not password:
        return "Malformed credentials", False, 400

    # look up header in mongo
    try:
        data = look_up_user(username=username)
        if not data.get("username", "") == username:
            return "Not Authorised", False, 401
    except pymongo.errors.PyMongoError as e:
        print(e)
        return "Internal Error", False, 500

    if hash_password(password, salt=data.get("salt", "")) == data.get("key", ""):
        return "", True, 200
    else:
        print("")
        for key, value in locals().items():
            print(key, value)
        return "Access Denied", False, 403
