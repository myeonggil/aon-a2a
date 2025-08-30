from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)
from litestar.testing import AsyncTestClient
from aon_a2a.main import app


app.debug = True

async def test_login_success():
    async with AsyncTestClient(app=app) as client:
        params = {"email": "mgju"}
        response = await client.get("/test/login", params=params)
        assert response.status_code == HTTP_200_OK
        assert response.json()["token"]


async def test_login_invalid_param():
    async with AsyncTestClient(app=app) as client:
        params = {"emails": "mgju"}
        response = await client.get("/test/login", params=params)
        assert response.status_code == HTTP_400_BAD_REQUEST
