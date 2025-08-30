from litestar.middleware import (
   AbstractAuthenticationMiddleware,
   AuthenticationResult,
)
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException

from aon_a2a.models import User
from aon_a2a.configs import config

import jwt, time


class AONAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self,
        connection: ASGIConnection
    ) -> AuthenticationResult:
        # do something here.
        auth_header = connection.headers.get("Authorization")
        if not auth_header:
            raise NotAuthorizedException()

        decoded_token = jwt.decode(
            jwt=auth_header,
            key=config["JWT_SECRET"],
            algorithms=config["JWT_ALGORITHM"]
        )
        if decoded_token["expired_at"] < int(time.time()):
            raise NotAuthorizedException()

        user = User(
            user_id=decoded_token["user_id"],
            name=decoded_token["name"],
            expired_at=decoded_token["expired_at"]
        )
        return AuthenticationResult(user=user, auth=None)
