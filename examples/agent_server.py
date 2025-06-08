import uvicorn

from examples.agent_executor import AONAgentExecutor

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill


# if __name__ == '__main__':
agent_skills = [
    AgentSkill(
        id="cloud_assistant",
        name="Cloud Assistant",
        description="Provide AWS Cloud detailed information.",
        tags=["AWS", "aws", "cloud", "Cloud"],
        examples=[
            # "IAM의 용도는 무엇이며 어떤 방식으로 사용해야 할까?",
            # "Cloud서비스를 효율적으로 운영하려면 어떻게 해야할까?"
        ]
    ),
    AgentSkill(
        id="IaC_assistant",
        name="IaC Assistant",
        description="Provide IaC like Terraform system information.",
        tags=["IaC", "Terraform", "terraform"],
        examples=[
            # "IaC의 장단점이 뭐야?",
            # "IaC를 효율적으로 관리하려면 어떻게 해야할까?"
        ]
    )
]

agent_card = AgentCard(
    name="AON Agent",
    description="AON Assistant",
    url="http://localhost:9999/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=agent_skills
)

request_handler = DefaultRequestHandler(
    agent_executor=AONAgentExecutor(),
    task_store=InMemoryTaskStore()
)

agent_server = A2AStarletteApplication(
    agent_card=agent_card, http_handler=request_handler
)
uvicorn.run(agent_server.build(), host="0.0.0.0", port=9999)
