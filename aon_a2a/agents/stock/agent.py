# import os
# import json
# from pathlib import Path
# from typing import Annotated, Literal
# from autogen import AssistantAgent, UserProxyAgent
# from autogen.coding import LocalCommandLineCodeExecutor
# from aon_a2a.configs import config

# # Configure Groq
# # Can I use multiple model?
# # Can I define multiple assistant?
# config_list = [{
#     "model": "llama-3.3-70b-versatile",
#     "api_key": config.get("GROQ_API_KEY"),
#     "api_type": "groq"
# }]

# # Create a directory to store code files from code executor
# # work_dir = Path("coding")
# # work_dir.mkdir(exist_ok=True)
# # code_executor = LocalCommandLineCodeExecutor(work_dir=work_dir)
# # Create the agent for tool calling
# chatbot = AssistantAgent(
#     name="chatbot",
#     system_message="""For currency exchange and weather forecasting tasks,
#         only use the functions you have been provided with.
#         Output 'HAVE FUN!' when an answer has been provided.""",
#     llm_config={"config_list": config_list},
# )

# # Define weather tool
# def get_current_weather(location: str, unit: str = "fahrenheit"):
#     """Get the weather for some location"""
#     weather_data = {
#         "berlin": {"temperature": "13"},
#         "istanbul": {"temperature": "40"},
#         "san francisco": {"temperature": "55"}
#     }
    
#     location_lower = location.lower()
#     if location_lower in weather_data:
#         return json.dumps({
#             "location": location.title(),
#             "temperature": weather_data[location_lower]["temperature"],
#             "unit": unit
#         })
#     return json.dumps({"location": location, "temperature": "unknown"})

# # Create an AI assistant that uses the weather tool
# assistant = AssistantAgent(
#     name="groq_assistant",
#     system_message="""You are a helpful AI assistant who can:
#     - Use weather information tools
#     - Analyze and explain results""",
#     llm_config={"config_list": config_list}
# )

# # Create a user proxy agent that only handles code execution
# user_proxy = UserProxyAgent(
#     name="user_proxy",
#     is_termination_msg=lambda x: x.get("content", "") and "HAVE FUN!" in x.get("content", ""),
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=1,
# )

# # Currency Exchange function

# CurrencySymbol = Literal["USD", "EUR"]

# # Define our function that we expect to call


# def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
#     if base_currency == quote_currency:
#         return 1.0
#     elif base_currency == "USD" and quote_currency == "EUR":
#         return 1 / 1.1
#     elif base_currency == "EUR" and quote_currency == "USD":
#         return 1.1
#     else:
#         raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


# # Register the function with the agent


# @user_proxy.register_for_execution()
# @chatbot.register_for_llm(description="Currency exchange calculator.")
# def currency_calculator(
#     base_amount: Annotated[float, "Amount of currency in base_currency"],
#     base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
#     quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
# ) -> str:
#     quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
#     return f"{format(quote_amount, '.2f')} {quote_currency}"


# # Weather function


# # Example function to make available to model
# def get_current_weather(location, unit="fahrenheit"):
#     """Get the weather for some location"""
#     if "chicago" in location.lower():
#         return json.dumps({"location": "Chicago", "temperature": "13", "unit": unit})
#     elif "san francisco" in location.lower():
#         return json.dumps({"location": "San Francisco", "temperature": "55", "unit": unit})
#     elif "new york" in location.lower():
#         return json.dumps({"location": "New York", "temperature": "11", "unit": unit})
#     else:
#         return json.dumps({"location": location, "temperature": "unknown"})


# # Register the function with the agent


# @user_proxy.register_for_execution()
# @chatbot.register_for_llm(description="Weather forecast for US cities.")
# def weather_forecast(
#     location: Annotated[str, "City name"],
# ) -> str:
#     weather_details = get_current_weather(location=location)
#     weather = json.loads(weather_details)
#     return f"{weather['location']} will be {weather['temperature']} degrees {weather['unit']}"


# # Start the conversation
# # start the conversation
# res = user_proxy.initiate_chat(
#     chatbot,
#     message="What's the weather in New York and can you tell me how much is 123.45 EUR in USD so I can spend it on my holiday? Throw a few holiday tips in as well.",
#     summary_method="reflection_with_llm",
# )

# print(f"LLM SUMMARY: {res.summary['content']}")

############# Try it! #############
# First, LLM Agent register
# Second, Is possible Sock API?
# Third, Is possible News API?
# Fourth, Is possible checking volatility?
# Last, Is possible reporting of result?

from aon_a2a.configs import config

from typing import Annotated, Literal

from autogen import AssistantAgent, UserProxyAgent


llm_config = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": config.get("GROQ_API_KEY"),
    "api_type": "groq"
}]
assistant = AssistantAgent(
    name="chatbot",
    system_message="""For currency exchange and weather forecasting tasks,
        only use the functions you have been provided with.
        Output 'HAVE FUN!' when an answer has been provided.""",
    llm_config={"config_list": llm_config},
)
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and "HAVE FUN!" in x.get("content", ""),
    human_input_mode="ALWAYS",
    code_execution_config=False,
    max_consecutive_auto_reply=1,
)

@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Geo location calculator")
def get_now_location(location: Annotated[str, "City name"]):
    print("location")


@user_proxy.register_for_execution()
@assistant.register_for_llm(description="Weather location calculator")
def get_now_weather(location: Annotated[str, "City name"]):
    print("weather")


res = user_proxy.initiate_chat(
    assistant,
    message="You are a helpful AI assistant who can: \
    - Use weather information tools",
    summary_method="reflection_with_llm",
)