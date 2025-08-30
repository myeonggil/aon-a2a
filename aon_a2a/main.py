import asyncio

from typing import Any

from aon_a2a.database.connection import AsyncSession, get_session
from aon_a2a.auth import AONAuthenticationMiddleware
from aon_a2a.models import User, AuthResponse, ChatResponse
from aon_a2a.utils import create_token

from litestar import Litestar, get, post, Controller, Request
from litestar.middleware import DefineMiddleware
from litestar.response import Stream
from litestar.serialization import encode_msgpack
from litestar.di import Provide

# Litestar - manual auth setup

class AONA2A(Controller):

    path = "/test"

    @get(
        path="/login",
        dependencies={
            "session": Provide(get_session)
        },
    )
    async def get_auth_token(
        self,
        email: str,
        session: AsyncSession,
    ) -> AuthResponse:
        if not email:
            raise Exception("Email")

        token = create_token(1, "mgju")
        return AuthResponse(token=token)

    @post(
        path="/chat",
        dependencies={
            "session": Provide(get_session)
        },
        middleware=[DefineMiddleware(AONAuthenticationMiddleware, exclude="schema")]
    )
    async def response_chat(
        self,
        request: Request[User, Any, Any],
        session: AsyncSession,
    ) -> ChatResponse:
        user = request.user
        return ChatResponse(content="Hello World!")

    @post(
        path="/stream",
        dependencies={
            "session": Provide(get_session)
        },
        middleware=[DefineMiddleware(AONAuthenticationMiddleware, exclude="schema")]
    )
    async def stream_chat(
        self,
        request: Request[User, Any, Any],
        session: AsyncSession,
    ) -> Stream:
        user = request.user
        async def my_generator():
            res = "hello world"
            for t in res:
                await asyncio.sleep(0.01)
                yield encode_msgpack({"current_time": 10})
        return Stream(my_generator(), media_type="text/plain")


app = Litestar(route_handlers=[AONA2A])
