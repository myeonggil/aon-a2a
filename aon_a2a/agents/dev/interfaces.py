from abc import ABC, abstractmethod


class AgentInterface(ABC):

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
