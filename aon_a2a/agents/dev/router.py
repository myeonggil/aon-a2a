import asyncio

from litestar import Litestar, get, post, Controller, Request
from litestar.response import Stream
from litestar.serialization import encode_msgpack
from litestar.di import Provide

from aon_a2a.agents.dev.service import DevelopmentKitService
from aon_a2a.models import ChatResponse


async def get_development_kit_service():
    return DevelopmentKitService()


class DevAgentRouter(Controller):
    
    """
        AONA2A(Advanced Open Network Agent to Agent)
        Workflow
    """

    path = "/agent"

    @get(
        path="/chat",
        dependencies={
            "session": Provide(get_development_kit_service)
        },
        # middleware=[DefineMiddleware(AONAuthenticationMiddleware, exclude="schema")]
    )
    async def response_chat(
        self,
        # request: Request[User, Any, Any],
        session: DevelopmentKitService,
    ) -> ChatResponse:
        print(session.development_kit_repository)
        return ChatResponse(content="Hello world")

    @post(
        path="/stream",
        dependencies={
            "session": Provide(get_development_kit_service)
        },
        # middleware=[DefineMiddleware(AONAuthenticationMiddleware, exclude="schema")]
    )
    async def stream_chat(
        self,
        # request: Request[User, Any, Any],
        session: DevelopmentKitService,
    ) -> Stream:
        async def my_generator():
            res = "hello world"
            for t in res:
                await asyncio.sleep(0.1)
                yield encode_msgpack({"current_time": t})
        return Stream(my_generator(), media_type="text/plain")
