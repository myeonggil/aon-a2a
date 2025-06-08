from typing import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class AONAgent:

    async def invoke(self) -> str:
        return "AON Agent"


class AONAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = AONAgent()

    @override
    async def execute(self, context, event_queue):
        result = await self.agent.invoke()
        event_queue.enqueue_event(new_agent_text_message(result))

    @override
    async def cancel(self, context, event_queue):
        raise Exception("cancel not supported")
