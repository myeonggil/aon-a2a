############# Try it! #############
# First, LLM Agent register
# Second, Is possible Sock API?
# Third, Is possible News API?
# Fourth, Is possible checking volatility?
# Last, Is possible reporting of result?

from aon_a2a.configs import config
from aon_a2a.agents.stock.models import AssistantPrompt

from typing import Annotated

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
                # @self.user_proxy.register_for_execution()
                # @assistant.register_for_llm(description=description)
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    # for name, param in sig.parameters.items():
                    #     if param.default is not inspect.Parameter.empty:
                    #         print(f"  {name} = {param.default}")
                    return await func(**kwargs)
                     # 에이전트를 함수의 속성으로 추가
                wrapper = async_wrapper
                wrapper.agent = agent
                wrapper.agent_type = "assistant"
                return wrapper
            else:
                @self.user_proxy.register_for_execution()
                @assistant.register_for_llm(description=description)
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # for name, param in sig.parameters.items():
                    #     if param.default is not inspect.Parameter.empty:
                    #         print(f"  {name} = {param.default}")
                    return func(*args, **kwargs)
                return wrapper
        return decorator

    def create_group_chat_manager(self):
        # 그룹 채팅 생성
        self.group_chat = GroupChat(
            agents=[unique_assistant.assistant for unique_assistant in self.assistants],
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

    def start_test(self, prompt: str = None):
        res = self.user_proxy.initiate_chat(
            self.manager,
            message="""
                너는 단순한 대화용 어시스턴트야.
                아래의 규칙을 반드시 지키고 <query></query>사이에 입력된 질문에 대해 답변을 해야해.

                <query>안녕?</query>
            """,
            summary_method="reflection_with_llm",
            # summary_method="last_msg",
            max_turns=4
        )
        return res

# generator_assistant = AssistantAgent(
#     name="generator_assistant",
#     system_message="""
#         너는 금융 분석 리포트 작성 전문가야. 입력된 주가 분석 정보와 관련 뉴스 요약을 바탕으로 
#         전문적인 PDF 리포트를 작성해줘. 문서는 다음과 같은 구조를 따라:
#         1. 기업 개요
#         2. 분석 대상 기간
#         3. 주가 상승/하락 요약
#         4. 주요 뉴스와 해석
#         5. 결론 및 인사이트
#         리포트는 그래프와 표를 포함하고, 한글 또는 영어로 포맷팅 가능해야 해.
#     """,
#     llm_config=llm_config,
# )

agent = Agent(None)
agent.register_assistant(
    "first",
    "first",
    """
        너는 채팅에 도움을 주는 어시스턴트야
        first_reply라는 함수를 사용해
        잘 답변해줘
    """
)
agent.register_assistant(
    "second",
    "second",
    """
        너는 채팅에 잘 답변해 주는 어시스턴트야
        second_reply라는 함수를 사용해
        잘 답변해줘
    """
)
agent.set_user_proxy()
agent.create_group_chat_manager()


@agent.register_func_tool("first", "chatting bot one")
async def first_reply(
    reply: Annotated[str, "about reply in Korea"],
):
    return f"나의 대답은 {reply}"

@agent.register_func_tool("second", "chatting next bot two")
async def second_reply(
    reply: Annotated[str, "about reply in Korea"],
):
    return f"나의 대답은 {reply}"

res = agent.start_test()
for msg in agent.group_chat.messages[-3:]:  # 마지막 3개 메시지
    if msg.get("name"):
        print(f"{msg['name']}: {msg['content']}")

for data in res.chat_history:
    print(data)
