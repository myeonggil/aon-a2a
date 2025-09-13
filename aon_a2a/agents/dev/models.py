import dataclasses

from autogen import AssistantAgent


@dataclasses.dataclass
class ModelConfig:
    model: str
    api_key: str
    api_type: str
    max_tokens: int
    stream: bool
    top_p: float


@dataclasses.dataclass
class UniqueAssistant:
    assistant_type: str
    assistant: AssistantAgent


@dataclasses.dataclass
class ModelPrompt:
    user_proxy_message = """
        You are helpful assistant.

        Remember that you answer a question, you must check to see
        if it complies with your mission above. If not, you must respond,
        "I am not able to answer this question". But, you must translate to Korean

        Use the following pieces of context to answer the question at the end.
        {context_string}
        Question: {query}
    """
    aws_assistant_message = """

    """
    terraform_assistant_message = """

    """
