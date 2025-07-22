############# Try it! #############
# First, LLM Agent register
# Second, Is possible Sock API?
# Third, Is possible News API?
# Fourth, Is possible checking volatility?
# Last, Is possible reporting of result?
import requests

from aon_a2a.configs import config

from typing import Annotated, Literal, Dict, Any
from datetime import datetime

from autogen import (
    AssistantAgent,
    UserProxyAgent,
    LLMConfig,
    ConversableAgent,
    register_function,
    GroupChat,
    GroupChatManager
)
from weasyprint import HTML, CSS


llm_config = LLMConfig(
    model="llama-3.3-70b-versatile",
    api_key=config.get("GROQ_API_KEY"),
    api_type="groq",
    max_tokens=1000,
    stream=True
)

stock_assistant = AssistantAgent(
    name="stock_assistant",
    system_message="""
        당신은 주식 데이터 수집 전문가입니다.
        수집된 데이터를 명확하고 읽기 쉽게 포맷팅해주세요.
    """,
    llm_config=llm_config,
)

news_assistant = AssistantAgent(
    name="news_assistant",
    system_message="""
        당신은 뉴스 수집 전문가입니다.
        수집된 데이터를 명확하고 읽기 쉽게 포맷팅해주세요.
    """,
    llm_config=llm_config,
)

generator_assistant = AssistantAgent(
    name="generator_assistant",
    system_message="""
        당신은 pdf파일 생성 전문가입니다.
        수집된 데이터를 명확하고 읽기 쉽게 포맷팅해주세요.
    """,
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=10,
)

@user_proxy.register_for_execution()
@stock_assistant.register_for_llm(description="Geo location calculator")
def get_now_location(location: Annotated[str, "City name"]):
    return f"그 도시 이름은 {location}입니다."


@user_proxy.register_for_execution()
@news_assistant.register_for_llm(description="Weather location calculator")
def get_now_weather(location: Annotated[str, "City name"]):
    return f"{location} 날씨는 37도입니다."


@user_proxy.register_for_execution()
@generator_assistant.register_for_llm(description="PDF information creation")
def get_pdf_information(pdf_information: Annotated[str, "PDF information"]):
    data = HTML(string=pdf_information).write_pdf("./report.pdf")
    return True


# 그룹 채팅 생성
group_chat = GroupChat(
    agents=[user_proxy, stock_assistant, news_assistant, generator_assistant],
    messages=[],
    max_round=10,
    allow_repeat_speaker=False,
    # speaker_selection_method="round_robin"
)

# 그룹 채팅 매니저
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
    silent=False
)

res = user_proxy.initiate_chat(
    manager,
    message="""
        삼성전자의 2024년 6월 주식 동향에 대해 분석해줘

        단계:
        1. 수집된 데이터를 사용자 친화적으로 포맷팅
        2. 날씨 상황에 맞는 조언 제공

        완료되면 TERMINATE로 마무리해주세요.
    """,
    # summary_method="reflection_with_llm",
    # summary_method="last_msg",
    # max_turns=1
)

result_messages = []
for msg in group_chat.messages[-3:]:  # 마지막 3개 메시지
    if msg.get("name") in ["chatbot"]:
        result_messages.append(f"{msg['name']}: {msg['content']}")

print("!" * 100)
print("\n\n".join(result_messages))
print(len(res.chat_history))
print("!" * 100)
