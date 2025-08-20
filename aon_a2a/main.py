import msgspec

from typing import Annotated, Optional, Any
from dataclasses import dataclass

from litestar import Litestar, get, post, Controller, Request
from litestar.security.jwt import JWTAuth, Token
from litestar.dto import MsgspecDTO
from litestar.params import Parameter
from litestar.di import Provide

# Litestar - manual auth setup
from litestar.middleware import AbstractAuthenticationMiddleware
import jwt


# class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
#     async def authenticate_request(self, connection):
#         token = connection.headers.get("Authorization", "").replace("Bearer ", "")
#         if token:
#             try:
#                 payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#                 return await get_user_by_id(payload["user_id"])
#             except jwt.JWTError:
#                 return None
#         return None



async def varify_authentication(headers: dict):
    return True


@dataclass
class CustomToken(Token):
    token_flag: bool = False


class Inside(msgspec.Struct):
    name: Optional[str] = None


class Response(msgspec.Struct):
    content: str


class RequestResponse(Controller):

    path = "/test"

    @get(
        path="/inside",
        dependencies={"local_dependency": Provide(varify_authentication)}
    )
    async def inside(self, inside: Inside, local_dependency: bool = False) -> Response:
        print(local_dependency)
        return Response(content="Hello World!")

    @post(path="/outside")
    async def outside(self, request: Request) -> Response:
        return Response(content="Hello World!")


app = Litestar(route_handlers=[RequestResponse])
