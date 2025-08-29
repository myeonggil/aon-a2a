from typing import Any

from aon_a2a.database.connection import AsyncSession, get_session
from aon_a2a.auth import MyAuthenticationMiddleware, DefineMiddleware
from aon_a2a.models import User, AuthResponse, ChatResponse
from aon_a2a.utils import create_token

from litestar import Litestar, get, post, Controller, Request
from litestar.di import Provide

# Litestar - manual auth setup

class AonA2A(Controller):

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
        print(email)
        if not email:
            raise Exception("Email")

        token = create_token(1, "mgju")
        return AuthResponse(token=token)

    @post(
        path="/chat",
        dependencies={
            "session": Provide(get_session)
        },
        middleware=[DefineMiddleware(MyAuthenticationMiddleware, exclude="schema")]
    )
    async def chat_with_bot(
        self,
        request: Request[User, Any, Any],
        session: AsyncSession,
    ) -> ChatResponse:
        user = request.user
        return ChatResponse(content="Hello World!")


app = Litestar(route_handlers=[AonA2A])
