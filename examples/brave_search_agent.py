from python_a2a import (
    A2AServer,
    skill,
    agent,
    run_server,
    TaskState,
    TaskStatus
)

import os
import requests
import logging


@agent(
    name="Brave Search Agent",
    description="Performs internet search using Brave Search API",
    version="1.0.0",
    url="https://symaon.com"
)
class BraveSearchAgent(A2AServer):
    pass
