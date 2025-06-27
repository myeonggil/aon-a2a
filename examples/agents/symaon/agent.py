from typing import AsyncGenerator

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from aon_a2a.configs import config


class SymaonAgent:
    def __init__(self):
        self.model = ChatGroq(
            api_key=config["GROQ_API_KEY"],
            model="llama-3.3-70b-versatile",
            temperature=0.7, # or 0.05?
            max_tokens=512,
            timeout=5,
        )

    async def stream(self, context_string: str, query: str) -> AsyncGenerator[str, None]:
        messages = [
            SystemMessage(
                content=f"""
                    You are helpful assistant.

                    Remember that you answer a question, you must check to see 
                    if it complies with your mission above. If not, you must respond, 
                    "I am not able to answer this question". But, you must translate to Korean

                    Use the following pieces of context to answer the question at the end.
                    {context_string}
                """
            ),
            SystemMessage(
                content="Keep all responses under 512 tokens."
            )
        ]

        messages.append(
            HumanMessage(
                content=f"""Question: {query}"""
            )
        )

        async for chunk in self.model.astream(messages):
            # Return the text content block.
            if hasattr(chunk, 'content') and chunk.content:
                yield {'content': chunk.content, 'done': False}
        yield {'content': '', 'done': True}

    async def ainvoke(self, context_string: str, query: str) -> str:
        messages = [
            SystemMessage(
                content=f"""
                    You are helpful assistant.

                    Remember that you answer a question, you must check to see 
                    if it complies with your mission above. If not, you must respond, 
                    "I am not able to answer this question". But, you must translate to Korean

                    Use the following pieces of context to answer the question at the end.
                    {context_string}
                """
            ),
            SystemMessage(
                content="Keep all responses under 512 tokens."
            )
        ]

        messages.append(
            HumanMessage(
                content=f"""Question: {query}"""
            )
        )

        response = await self.model.ainvoke(messages)
        return response.content
