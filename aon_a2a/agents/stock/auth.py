import requests
import json
import asyncio

from datetime import datetime, timedelta

from aon_a2a.configs import config
from aon_a2a.agents.stock.repository import UserRepository


class OAuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.headers = {
            "content-type": "application/json"
        }
        self.body = {
            "grant_type": "client_credentials",
            "appkey": config["STOCK_APP_KEY"], 
            "appsecret": config["STOCK_APP_SECRET"]
        }
        path = "oauth2/tokenP"
        self.url = f"{config['STOCK_APP_DOMAIN']}/{path}"

    def get_access_token(self):
        try:
            res = requests.post(
                self.url,
                headers=self.headers,
                data=json.dumps(self.body)
            )
            access_token = res.json()["access_token"]
        except Exception as err:
            print("Try after 1 minutes")
            access_token = None
        return access_token

    async def get_auth(self):
        user = await self.user_repository.get_user()
        if user:
            if not user.access_token:
                access_token = self.get_access_token()
                if access_token:
                    await self.user_repository.update_user(access_token)
            elif user.updated_at < datetime.now():
                access_token = self.get_access_token()
                if access_token:
                    await self.user_repository.update_user(access_token)
            else:
                user = await self.user_repository.get_user()
                access_token = user.access_token
        else:
            await self.user_repository.create_user()
            access_token = self.get_access_token()
            if access_token:
                await self.user_repository.update_user(access_token)
        return access_token
