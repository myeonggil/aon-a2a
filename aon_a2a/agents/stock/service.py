import requests
import json
import asyncio

from datetime import datetime, timedelta

from aon_a2a.configs import config
from aon_a2a.agents.stock.models import (
    RequestHeader,
    StockInfo,
    ResponseBody,
    ResponseBodyoutput
)
from aon_a2a.agents.stock.repositories import (
    UserRepository,
    StockRepository
)


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

    async def get_last_date_price(self, access_token: str, stock_code: str):
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = RequestHeader(
            authorization=access_token,
            appkey=config["STOCK_APP_KEY"],
            appsecret=config["STOCK_APP_SECRET"],
            tr_id="FHKST01010100",
            custtype="P"
        ).to_dict()

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
            output = ResponseBodyoutput(**result["output"])
        except Exception as err:
            print(err)
            output = {}
        return output

    async def get_lasted_date_price(self,
        access_token: str,
        stock_code: str,
        start_date: str,
        end_date: str,
        duration: str
    ):
        """
        duration -> D:일봉 W:주봉, M:월봉, Y:년봉
        """
        path = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        headers = RequestHeader(
            authorization=access_token,
            appkey=config["STOCK_APP_KEY"],
            appsecret=config["STOCK_APP_SECRET"],
            tr_id="FHKST03010100",
            custtype="P"
        ).to_dict()

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # J:KRX, NX:NXT, UN:통합
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": duration,
            "FID_ORG_ADJ_PRC": "1"  # 0: 수정주가, 1: 원주가
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


class StockService:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    async def get_stock_code_by_name(self, stock_name: str) -> StockInfo:
        if not stock_name:
            raise Exception("Check the name")

        raw_stock = await self.stock_repository.get_stock_by_name(stock_name)
        stock = StockInfo(
            stock_name=raw_stock.stock_name,
            stock_code=raw_stock.stock_code,
            market_division=raw_stock.market_division
        )
        return stock


# async def main():
#     user_repository = UserRepository()
#     kis_service = KISService(user_repository)
#     access_token = await kis_service.get_auth()
#     # result = await kis_service.get_last_date_price(access_token, "005930")
#     result = await kis_service.get_lasted_date_price(
#         access_token=access_token,
#         stock_code="005930",
#         start_date="20250701",
#         end_date="20250720",
#         duration="D"
#     )
#     print(result)

# if __name__ == '__main__':
#     asyncio.run(main())
