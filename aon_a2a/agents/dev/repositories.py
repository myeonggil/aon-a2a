import os

from aon_a2a.database.connection import get_motor_client, AsyncMongoClient
from aon_a2a.agents.dev.interfaces import IDevelopmentKit
from aon_a2a.configs import config

from nomic import embed, login
os.environ["TOKENIZERS_PARALLELISM"] = "true"
login(token=config["NOMIC_API_TOKEN"])


class DevelopmentKitRepository(IDevelopmentKit):
    def __init__(self, client: AsyncMongoClient = get_motor_client()):
        self.client = client
        self.db = self.client["chatbot"]
        self.collection = self.db["chat_history"]

    async def get_embedded_query(self, query: str, precision: str = "float32") -> list[float | int]:
        response = embed.text([query])
        return response['embeddings'][0]

    async def get_context_string_from_docs(self, embedded_query: list[float | int]) -> str:
        context_docs = await self.search_vector(embedded_query=embedded_query)
        context_string = " ".join([doc["text"] for doc in context_docs])
        return context_string

    async def search_vector(self, embedded_query: str):
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": embedded_query,
                    "path": "embedding",
                    "exact": True,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1
                }
            }
        ]
        array_of_results = []
        async for doc in await self.collection.aggregate(pipeline=pipeline):
            array_of_results.append(doc)
        return array_of_results

    async def vector_to_text(self, embedded_query: list[float]):
        return await super().vector_to_text(embedded_query)

    async def text_to_vector(self, query: str):
        return await super().text_to_vector(query)


development_kit_repository = DevelopmentKitRepository()
