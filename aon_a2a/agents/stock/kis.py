# from numbers_parser import Document
# doc = Document("./code.numbers")
# sheets = doc.sheets
# tables = sheets[0].tables
# rows = tables[0].rows()
# stock_item = rows[1][1].value
# stock_code = int(rows[1][0].value)
# market_division = rows[1][2].value

# stock_info = StockInfo(market_division=market_division, stock_code=stock_code)
# stock = Stock(stock_name=stock_item, stock_info=stock_info)
# print(stock)

# API
import requests
import asyncio

from aon_a2a.agents.stock.auth import get_auth
from aon_a2a.database.connection import async_session, AsyncSession
from aon_a2a.database.schema import User
from aon_a2a.configs import config

from sqlalchemy.future import select



async def get_price():
    async with async_session() as session:
        session: AsyncSession
        result = await session.execute(select(User).where(User.name == "mgju"))
        user = result.scalar_one_or_none()

        if user:
            # 있으면 업데이트
            access_token = user.access_token
            # session.add(user)는 생략 가능
        else:
            # 없으면 insert
            access_token = await get_auth()

    path = "/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": config["STOCK_APP_KEY"],
        "appsecret": config["STOCK_APP_SECRET"],
        "tr_id": "FHKST01010100",   # ???
        "custtype": "P",    # "B" is buessiness
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # "J" is KRX, "NX" is NXT, "UN" is 통합
        "FID_INPUT_ISCD": "005930"    # 종목코드
    }

    res = requests.get(
        url=f"{config['STOCK_APP_DOMAIN']}/{path}",
        headers=headers,
        params=params
    )

    try:
        result = res.json()
        if result["msg_cd"] == "EGW00123":
            await get_auth()
        print(result)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    asyncio.run(get_price())
