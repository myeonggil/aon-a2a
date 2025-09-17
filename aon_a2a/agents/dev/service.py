from aon_a2a.agents.dev.repositories import development_kit_repository
from aon_a2a.agents.dev.agent import Agent


class DevelopmentKitService:
    def __init__(self):
        self.development_kit_repository = development_kit_repository
        self.agent = Agent()

    async def get_agent_response(self):
        pass

    async def get_agent_stream(self):
        # How to make stream agent response?
        pass
