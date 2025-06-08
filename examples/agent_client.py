import httpx
import asyncio

from a2a.client import A2AClient
from typing import Any
from uuid import uuid4
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    SendStreamingMessageRequest
)


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client=httpx_client,
            base_url="http://localhost:9999"
        )

        send_message_payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "AWS와 Terraform의 관계에 대해 알려줘"
                    }
                ],
                "messageId": uuid4().hex
            }
        }
        request = SendMessageRequest(
            params=MessageSendParams(**send_message_payload)
        )
        response = await client.send_message(request)
        print(response.model_dump(mode="json", exclude_none=True))

        streaming_request = SendStreamingMessageRequest(
            params=MessageSendParams(**send_message_payload)
        )
        streaming_response = client.send_message_streaming(
            request=streaming_request
        )
        async for chunk in streaming_response:
            print(chunk.model_dump(mode="json", exclude_none=True))


if __name__ == '__main__':
    asyncio.run(main())
