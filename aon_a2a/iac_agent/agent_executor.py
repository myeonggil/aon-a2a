from typing import override

from aon_a2a.iac_agent.agent import IaCAgent

from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_text_artifact


class IaCAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = IaCAgent()

    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        query = context.get_user_input()
        if not context.message:
            raise Exception("No message provided")

        async for event in self.agent.stream(context_string=None, query=query):
            message = TaskArtifactUpdateEvent(
                contextId=context.context_id,
                taskId=context.task_id,
                artifact=new_text_artifact(
                    name='current_result',
                    text=event['content']
                )
            )
            event_queue.enqueue_event(message)

    @override
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        raise Exception("cancel not supported")
