############# Try it! #############
# First, LLM Agent register
# Second, Is possible Sock API?
# Third, Is possible News API?
# Fourth, Is possible checking volatility?
# Last, Is possible reporting of result?

from aon_a2a.configs import config

from typing import Annotated, Literal

from autogen import AssistantAgent, UserProxyAgent
from weasyprint import HTML, CSS


llm_config = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": config.get("GROQ_API_KEY"),
    "api_type": "groq"
}]
assistant = AssistantAgent(
    name="chatbot",
    system_message="""You are a helpful AI assistant who can: 
    - Use weather information tools
    - Use location information tools
    - Use PDF creation tools""",
    llm_config={"config_list": llm_config},
)
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and "HAVE FUN!" in x.get("content", ""),
    human_input_mode="TERMINATE",
    code_execution_config=False,
    max_consecutive_auto_reply=1,
)

@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Geo location calculator")
def get_now_location(location: Annotated[str, "City name"]):
    return True


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Weather location calculator")
def get_now_weather(location: Annotated[str, "City name"]):
    return True


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="PDF information creation")
def get_pdf_information(pdf_information: Annotated[str, "PDF information"]):
    HTML(string=pdf_information).write_pdf("./report.pdf")
    return True


res = user_proxy.initiate_chat(
    assistant,
    message="""You can create one page amount pdf information
    Please create an HTML document with the following contents:
    - Article between titles
    - Content: Includes sales figures, charts, tables, etc.
    - Includes numerous CSS edits
    Please write in HTML format""",
    summary_method="reflection_with_llm",
)