############# Try it! #############
# First, LLM Agent register
# Second, Is possible Sock API?
# Third, Is possible News API?
# Fourth, Is possible checking volatility?
# Last, Is possible reporting of result?

from aon_a2a.configs import config
from aon_a2a.agents.stock.service import (
    KISService,
    StockService
)
from aon_a2a.agents.stock.naver_news import search_news
from aon_a2a.agents.stock.repositories import (
    UserRepository,
    StockRepository
)
from aon_a2a.agents.stock.models import AssistantPrompt

from typing import Annotated, Literal, Dict, Any
from datetime import datetime

from autogen import (
    AssistantAgent,
    UserProxyAgent,
    LLMConfig,
    ConversableAgent,
    register_function,
    GroupChat,
    GroupChatManager,
)
from weasyprint import HTML, CSS
from fastapi import FastAPI

app = FastAPI()


user_repository = UserRepository()
stock_repository = StockRepository()
kis_service = KISService(user_repository)
stock_service = StockService(stock_repository)


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
        너는 금융 데이터 분석 전문가야. 유저가 입력한 기업명과 기간을 기준으로 해당 기업의 
        주가 데이터를 수집하고, 기간 내 최고 상승 구간과 최고 하락 구간을 찾아. 
        각 구간의 시작일, 종료일, 상승/하락률을 정리해서 출력해줘. 
        추가로 해당 구간의 기술적 분석도 간단히 포함해줘.
        get_market_trend 함수를 사용하여 회사의 이름과 날짜나 기간이 확인되면 기간 혹은 날짜를 수집해 
        날짜 혹은 기간이 확인 되지 않으면 수집하지마.
        작업이 종료되면 TERMINATE로 마무리해줘.
    """,
    llm_config=llm_config,
)

news_assistant = AssistantAgent(
    name="news_assistant",
    system_message="""
        너는 경제 뉴스 분석 전문가야. 입력된 기업명과 특정 날짜 구간을 기준으로,
        주가 변화와 관련된 뉴스 기사를 검색하고, 주가 상승 또는 하락의 원인을 설명해주는 기사만 
        선별해서 정리해줘. 중복되거나 의미 없는 기사는 제외하고 핵심 내용을 요약해줘.
        get_news_event 함수를 사용하여 Question: 에 입력된 질문을 요약해서 수집해.
        작업이 종료되면 TERMINATE로 마무리해줘.
    """,
    llm_config=llm_config,
)

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
#         작업이 종료되면 TERMINATE로 마무리해줘.
#     """,
#     llm_config=llm_config,
# )

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=10,
)

@user_proxy.register_for_execution()
@stock_assistant.register_for_llm(description="Stock price calculator")
async def get_market_trend(
    stock_name: Annotated[str, "Company name to Korea language"],
    date: Annotated[str, "Specific requested date"] = None,
    duration: Annotated[str, "How long it lasted"] = None
):
    # You have to get stock code using stock name(name)
    """
    종목코드를 찾을 수 있다.
    기간별로 시세를 확인할 수 있다
    """
    access_token = await kis_service.get_auth()
    stock = await stock_service.get_stock_code_by_name(stock_name)
    results = await kis_service.get_last_date_price(access_token, stock.stock_code)
    return


@user_proxy.register_for_execution()
@news_assistant.register_for_llm(description="Stock news collector")
async def get_news_event(
    summary: Annotated[str, "Question summary to Korea language"]
):
    # You have to use search api with stock item and event combination
    return


# @user_proxy.register_for_execution()
# @generator_assistant.register_for_llm(description="PDF information creation")
# async def get_pdf_file(pdf_information: Annotated[str, "PDF information"]):
#     data = HTML(string=pdf_information).write_pdf("./report.pdf")
#     return True


# 그룹 채팅 생성
group_chat = GroupChat(
    agents=[user_proxy, stock_assistant, news_assistant],
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

# 프롬프트를 어떻게 작성해야할까? 유저의 입력을 잘 풀어서 설명하는 것이 목표
res = user_proxy.initiate_chat(
    manager,
    message="""
        너는 주식시장과 관련된 기사를 찾아서 보고서 형태의 PDF를 잘 만드는 어시스턴트야.
        아래의 규칙을 반드시 지키고 Question: 에 입력된 질문에 대해 답변을 해야해.

        다음 규칙은 반드시 지켜야해:
        - 수집된 데이터를 사용자 친화적으로 포맷팅

        Question: 2023년부터 2년동안 삼성전자 주식에 관련된 데이터와 뉴스 기사에 대해 분석해줘

        완료되면 TERMINATE로 마무리해주세요.
    """,
    # summary_method="reflection_with_llm",
    # summary_method="last_msg",
    # max_turns=1
)

result_messages = []
for msg in group_chat.messages[-3:]:  # 마지막 3개 메시지
    if msg.get("name") in ["stock_assistant", "news_assistant", "generator_assistant"]:
        result_messages.append(f"{msg['name']}: {msg['content']}")

print("!" * 100)
print("\n\n".join(result_messages))
print(len(res.chat_history))
print(res.cost)
print("!" * 100)
