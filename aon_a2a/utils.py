import jwt
import time

from aon_a2a.configs import config


def create_token(user_id: int, name: str) -> str:
    token = jwt.encode(
        payload={
            "user_id": user_id,
            "name": name,
            "expired_at": int(time.time() + 3600)   # Valid until after one hour
        },
        key=config["JWT_SECRET"],
        algorithm=config["JWT_ALGORITHM"]
    )
    return token
