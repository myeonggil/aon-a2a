# from aon_a2a.agents.dev.agent import Agent

# from typing import Annotated


# agent = Agent(None)
# agent.register_assistant(
#     "first",
#     "first",
#     """
#         너는 채팅에 도움을 주는 어시스턴트야
#         잘 답변해줘
#     """
# )
# agent.register_assistant(
#     "second",
#     "second",
#     """
#         너는 채팅에 잘 답변해 주는 어시스턴트야
#         잘 답변해줘
#     """
# )
# agent.set_user_proxy()
# agent.create_group_chat_manager()


# @agent.register_func_tool("first", "chatting bot one")
# async def test(
#     reply: Annotated[str, "about reply in Korea"],
# ):
#     return f"나의 대답은 {reply}"

# @agent.register_func_tool("second", "chatting next bot two")
# async def second_reply(
#     reply: Annotated[str, "about reply in Korea"],
# ):
#     return f"나의 대답은 {reply}"

# res = agent.start_test()
# print(res.chat_history)