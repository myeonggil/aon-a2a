import requests
import json
import asyncio

from datetime import datetime, timedelta

from aon_a2a.configs import config
from aon_a2a.agents.stock.repository import UserRepository


class KISService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _get_access_token(self):

        headers = {
            "content-type": "application/json"
        }
        params = {
            "grant_type": "client_credentials",
            "appkey": config["STOCK_APP_KEY"], 
            "appsecret": config["STOCK_APP_SECRET"]
        }
        path = "oauth2/tokenP"
        url = f"{config['STOCK_APP_DOMAIN']}/{path}"

        try:
            res = requests.post(
                url=url,
                headers=headers,
                data=json.dumps(params)
            )
            access_token = res.json()["access_token"]
        except Exception as err:
            print("Try after 1 minutes")
            access_token = None
        return access_token

    async def get_auth(self) -> str:
        user = await self.user_repository.get_user()
        if user:
            if not user.access_token:
                access_token = self._get_access_token()
                if access_token:
                    await self.user_repository.update_user(access_token)
            elif updated_at := user.updated_at:
                # TODO: first, check 1 minute
                # second, check validation
                time_diff = datetime.now() - updated_at
                if time_diff >= timedelta(days=1):
                    access_token = self._get_access_token()
                    if access_token:
                        await self.user_repository.update_user(access_token)
                else:
                    access_token = user.access_token
            else:
                user = await self.user_repository.get_user()
                access_token = user.access_token
        else:
            await self.user_repository.create_user()
            access_token = self._get_access_token()
            if access_token:
                await self.user_repository.update_user(access_token)
        return access_token

    async def get_price(self, access_token: str, stock_code: str):
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appkey": config["STOCK_APP_KEY"],
            "appsecret": config["STOCK_APP_SECRET"],
            "tr_id": "FHKST01010100",
            "custtype": "P",    # B business, P Personal

        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # J:KRX, NX:NXT, UN:통합
            "FID_INPUT_ISCD": stock_code
        }

        try:
            res = requests.get(
                url=f"{config['STOCK_APP_DOMAIN']}/{path}",
                headers=headers,
                params=params
            )
            result = res.json()
        except Exception as err:
            print(err)
            result = {}
        return result


# async def main():
#     user_repository = UserRepository()
#     kis_service = KISService(user_repository)
#     access_token = await kis_service.get_auth()
#     result = await kis_service.get_price(access_token, "005930")
#     print(result)

# if __name__ == '__main__':
#     asyncio.run(main())
