from aon_a2a.configs import config

from autogen import (
    AssistantAgent,
    UserProxyAgent,
    LLMConfig,
    GroupChat,
    GroupChatManager,
)

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable

import inspect
import functools


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



@dataclass
class ModelConfig:
    model: str
    api_key: str
    api_type: str
    max_tokens: int
    stream: bool
    top_p: float


@dataclass
class UniqueAssistant:
    assistant_type: str
    assistant: AssistantAgent


class Agent(AgentInterface):
    def __init__(self, model_config: ModelConfig):
        self.llm_config = LLMConfig(
            model="llama-3.3-70b-versatile",
            api_key=config.get("GROQ_API_KEY"),
            api_type="groq",
            max_tokens=1500,
            stream=True,
            top_p=0.9,
        )
        self.assistants: list[UniqueAssistant] = []
        self.user_proxy = None
        self.group_chat = None
        self.manager = None

    def register_assistant(self, assistant_type: str, name: str, system_message: str):
        is_possible = filter(lambda x: x.assistant_type == assistant_type, self.assistants)
        if not next(is_possible, None):
            assistant =  AssistantAgent(
                name=name,
                system_message=system_message,
                llm_config=self.llm_config,
            )
            unique_assistant = UniqueAssistant(
                assistant_type=assistant_type,
                assistant=assistant
            )
            self.assistants.append(unique_assistant)

    def set_user_proxy(
        self,
        name: str = "user_proxy",
        is_termination_msg: dict[str, any] = (
            lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE")
        ),
        human_input_mode: str = "NEVER",
        code_execution_config: bool = False,
        max_consecutive_auto_reply: int = 10
    ):
        user_proxy = UserProxyAgent(
            name=name,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
            code_execution_config=code_execution_config,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
        )
        self.user_proxy = user_proxy

    def register_func_tool(self, assistant_type: str, description: str):
        assistants = filter(lambda x: x.assistant_type == assistant_type, self.assistants)
        unique_assistant = next(assistants, None)
        if not unique_assistant:
            raise Exception("Please register assistant or check assistant type")

        assistant = unique_assistant.assistant
        def decorator(func: Callable):
            sig = inspect.signature(func)  # 함수 시그니처 가져오기
            if inspect.iscoroutinefunction(func):
                @self.user_proxy.register_for_execution()
                @assistant.register_for_llm(description=description)
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(**kwargs)
                return async_wrapper
            else:
                @self.user_proxy.register_for_execution()
                @assistant.register_for_llm(description=description)
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return wrapper
        return decorator

    def create_group_chat_manager(self):
        # 그룹 채팅 생성
        agents = [unique_assistant.assistant for unique_assistant in self.assistants]
        if not agents or not self.user_proxy:
            raise Exception("Register assistant or user proxy")
        agents.append(self.user_proxy)
        self.group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=10,
            allow_repeat_speaker=False,
            # speaker_selection_method="round_robin"
        )

        # 그룹 채팅 매니저
        self.manager = GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.llm_config,
            silent=True
        )

    def start_test(
            self,
            prompt: str = None,
            max_turns: int = None,
            summary_method: str = "last_msg",
        ):
        """
        summary_method: last_msg or reflection_with_llm
        """
        res = self.user_proxy.initiate_chat(
            self.manager,
            message="""
                너는 단순한 대화용 어시스턴트야.
                아래의 규칙을 반드시 지키고 <query></query>사이에 입력된 질문에 대해 답변을 해야해.

                <query>안녕?</query>
            """,
            summary_method=summary_method,
            max_turns=max_turns
        )
        return res
