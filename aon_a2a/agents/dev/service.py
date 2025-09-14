from aon_a2a.agents.dev.repositories import development_kit_repository
from aon_a2a.agents.dev.agent import Agent


class DevelopmentKitService:
    def __init__(self):
        self.development_kit_repository = development_kit_repository
        self.agent = Agent()
