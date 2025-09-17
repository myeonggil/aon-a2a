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
        dev_kit_service: DevelopmentKitService,
    ) -> ChatResponse:
        response = await dev_kit_service.get_agent_response()
        return response

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
        dev_kit_service: DevelopmentKitService,
    ) -> Stream:
        return Stream(dev_kit_service.get_agent_stream(), media_type="text/plain")
