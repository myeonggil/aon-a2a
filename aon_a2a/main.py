import msgspec

from typing import Annotated, Optional, Any
from dataclasses import dataclass

from aon_a2a.database.connection import AsyncSession, get_session
from aon_a2a.auth import validate_authentication

from litestar import Litestar, get, post, Controller, Request
from litestar.security.jwt import JWTAuth, Token
from litestar.dto import MsgspecDTO
from litestar.params import Parameter
from litestar.di import Provide

# Litestar - manual auth setup


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
        dependencies={
            "is_valid": Provide(validate_authentication),
            "session": Provide(get_session)
        }
    )
    async def inside(
        self,
        name: str,
        session: AsyncSession,
        is_valid: bool = False
    ) -> Response:
        return Response(content="Hello World!")

    @post(path="/outside")
    async def outside(self, request: Request) -> Response:
        return Response(content="Hello World!")


app = Litestar(route_handlers=[RequestResponse])
