from abc import ABC, abstractmethod


class IAgent(ABC):

    @abstractmethod
    def register_assistant(self, assistant_type: str, name: str, system_message: str):
        ...

    @abstractmethod
    def set_user_proxy(
        self,
        name: str,
        is_termination_msg: dict[str, any],
        human_input_mode: bool,
        code_execution_config: bool,
        max_consecutive_auto_reply: int
    ):
        ...

    @abstractmethod
    def register_func_tool(self, description: str):
        ...

    @abstractmethod
    def create_group_chat_manager(self):
        ...


class IDevelopmentKit(ABC):
    """
    This is for AWS and IaC quick guide
    """

    async def get_embedded_query(self, query: str):
        ...

    async def get_context_string_from_docs(self, embedded_query_vector: list[float, int]):
        ...

    async def search_vector(self, embedded_query_str: str):
        ...

    async def text_to_vector(self, query: str):
        ...

    async def vector_to_text(self, embedded_query: list[float]):
        ...
