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
    stream=True
)

# def get_geo_location(location: Annotated[str, "City name"]):
#     longitude, latitude =  37.5642135, 127.0016985
#     return f"{location} longitude is {longitude} and latitude is {latitude}"

# def get_now_weather(location: Annotated[str, "City name"]):
#     return f"There name is {location}"

# # 2. Agent for determining whether to run the tool
# with llm_config:
#     weather_agent = ConversableAgent(
#         name="weather_agent",
#         system_message="""You are a helpful AI assistant who can: 
#         - Use Weather information tools
#         - Use Geo information tools""",
#     )

# # 3. And an agent for executing the tool
# executor_agent = ConversableAgent(
#     name="executor_agent",
#     human_input_mode="NEVER",
# )

# # 4. Registers the tool with the agents, the description will be used by the LLM
# register_function(
#     get_geo_location,
#     caller=weather_agent,
#     executor=executor_agent,
#     description="Get the geographical location",
# )
# register_function(
#     get_now_weather,
#     caller=weather_agent,
#     executor=executor_agent,
#     description="Get the weather of location",
# )

# # 5. Two-way chat ensures the executor agent follows the suggesting agent
# chat_result = executor_agent.initiate_chat(
#     recipient=weather_agent,
#     message="How is weather in Korea and how about geographical location?",
#     max_turns=10,
# )

# print(chat_result.chat_history[-1]["content"])


llm_config = [{
    # "model": "llama-3.3-70b-versatile",
    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
    "api_key": config.get("GROQ_API_KEY"),
    "api_type": "groq"
}]
# assistant = AssistantAgent(
#     name="chatbot",
#     system_message="""You are a helpful AI assistant who can: 
#     - Use weather information tools
#     - Use location information tools
#     - Use PDF creation tools
    
#     You can create one page amount pdf information
#     Please create an HTML document with the following contents:
#     - Article between titles
#     - Content: Includes sales figures, charts, tables, etc.
#     - Includes numerous CSS edits
#     Please write in HTML format""",
#     llm_config={"config_list": llm_config},
# )
# user_proxy = UserProxyAgent(
#     name="user_proxy",
#     # is_termination_msg=lambda x: x.get("content", "") and "HAVE FUN!" in x.get("content", ""),
#     # human_input_mode="TERMINATE",
#     human_input_mode="NEVER",
#     code_execution_config=False,
#     max_consecutive_auto_reply=1,
# )

# @user_proxy.register_for_execution()
# @assistant.register_for_llm(description="Geo location calculator")
# def get_now_location(location: Annotated[str, "City name"]):
#     return {"status": True, "content": "Geo"}


# @user_proxy.register_for_execution()
# @assistant.register_for_llm(description="Weather location calculator")
# def get_now_weather(location: Annotated[str, "City name"]):
#     return {"status": True, "content": "Weather"}


# @user_proxy.register_for_execution()
# @assistant.register_for_llm(description="PDF information creation")
# def get_pdf_information(pdf_information: Annotated[str, "PDF information"]):
#     HTML(string=pdf_information).write_pdf("./report.pdf")
#     return True


# res = user_proxy.initiate_chat(
#     assistant,
#     message="How is weather USA and where is there?",
#     # summary_method="reflection_with_llm",
#     summary_method="last_msg",
#     max_turns=4
# )

# print(res.summary)
# print(res.chat_history)

# 날씨 API 호출 함수
def get_weather_data(city: str) -> Dict[str, Any]:
    """OpenWeatherMap API를 사용해 날씨 정보 가져오기"""
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": config.get("WEATHER_API_KEY"),
            "units": "metric",  # 섭씨 온도
            "lang": "kr"  # 한국어
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 필요한 정보만 추출
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return weather_info
        
    except requests.RequestException as e:
        return {"error": f"API 호출 실패: {str(e)}"}
    except KeyError as e:
        return {"error": f"데이터 파싱 실패: {str(e)}"}

# AutoGen 에이전트 설정
def create_weather_agents():
    """날씨 서비스를 위한 에이전트들 생성"""
    
    # 1. 사용자 프록시 에이전트 (사용자 대신 요청을 처리)
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        # code_execution_config={
        #     "work_dir": "weather_temp",
        #     "use_docker": False,
        # },
        code_execution_config=False,
    )
    
    # 2. 날씨 데이터 수집 에이전트
    weather_collector = AssistantAgent(
        name="weather_collector",
        llm_config={"config_list": llm_config, "temperature": 0},
        system_message="""당신은 날씨 데이터 수집 전문가입니다.
        사용자가 요청한 도시의 날씨 정보를 가져와서 정리해주세요.
        get_weather_data 함수를 사용해서 실시간 날씨 정보를 수집합니다.
        수집된 데이터를 명확하고 읽기 쉽게 포맷팅해주세요.""",
        function_map={"get_weather_data": get_weather_data}
    )
    
    # 3. 날씨 분석 및 조언 에이전트
    weather_advisor = AssistantAgent(
        name="weather_advisor",
        llm_config={"config_list": llm_config, "temperature": 0.3},
        system_message="""당신은 날씨 분석 및 조언 전문가입니다.
        날씨 데이터를 분석하여 사용자에게 유용한 조언을 제공해주세요.
        - 옷차림 추천
        - 활동 추천
        - 주의사항
        - 날씨 특징 분석
        친근하고 도움이 되는 조언을 해주세요."""
    )
    
    return user_proxy, weather_collector, weather_advisor

# 그룹 채팅 설정 및 실행
def run_weather_service(city: str) -> str:
    """날씨 서비스 실행"""
    
    user_proxy, weather_collector, weather_advisor = create_weather_agents()
    
    # 그룹 채팅 생성
    group_chat = GroupChat(
        agents=[user_proxy, weather_collector, weather_advisor],
        messages=[],
        max_round=10
    )
    
    # 그룹 채팅 매니저
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": llm_config, "temperature": 0},
        silent=False
    )
    
    # 날씨 요청 메시지
    weather_request = f"""
    {city} 지역의 실시간 날씨 정보를 수집하고 분석해주세요.
    
    단계:
    1. get_weather_data('{city}') 함수를 사용해서 날씨 데이터 수집
    2. 수집된 데이터를 사용자 친화적으로 포맷팅
    3. 날씨 상황에 맞는 조언 제공
    
    완료되면 TERMINATE로 마무리해주세요.
    """
    
    # 대화 시작
    user_proxy.initiate_chat(manager, message=weather_request)
    result_messages = []
    for msg in group_chat.messages[-3:]:  # 마지막 3개 메시지
        if msg.get("name") in ["weather_collector", "weather_advisor"]:
            result_messages.append(f"{msg['name']}: {msg['content']}")
    
    print("!" * 100)
    print("\n\n".join(result_messages))
    print("!" * 100)

run_weather_service("Seoul")
