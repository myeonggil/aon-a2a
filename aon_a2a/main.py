import msgspec

from typing import Annotated

from litestar import Litestar, get, post, Controller
from litestar.dto.msgspec_dto import MsgspecDTO


class Request(msgspec.Struct):
    name: Annotated[str, None]


class Response(msgspec.Struct):
    content: str


class RequestResponse(Controller):

    path = "/test"

    @get("/inside")
    async def inside(self, name: str) -> Response:
        print(name)
        return Response(content="Hello World!")

    @post("/outside")
    async def outside(self, request: Request) -> Response:
        print(request.name)
        return Response(content="Hello World!")


app = Litestar(route_handlers=[RequestResponse])
