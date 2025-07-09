import requests
import json

from aon_a2a.configs import config
from aon_a2a.database.connection import async_session, User, AsyncSession
from sqlalchemy.future import select


# Auth
async def get_auth():
    headers = {
        "content-type": "application/json"
    }
    body = {
        "grant_type": "client_credentials",
        "appkey": config["STOCK_APP_KEY"], 
        "appsecret": config["STOCK_APP_SECRET"]
    }
    path = "oauth2/tokenP"
    url = f"{config['STOCK_DOMAIN']}/{path}"
    res = requests.post(url, headers=headers, data=json.dumps(body))
    try:
        access_token = res.json()["access_token"]
        async with async_session() as session:
            session: AsyncSession
            result = await session.execute(select(User).where(User.name == "mgju"))
            user = result.scalar_one_or_none()

            if user:
                # 있으면 업데이트
                user.access_token = access_token
                # session.add(user)는 생략 가능
                print("✅ 사용자 업데이트됨")
            else:
                # 없으면 insert
                new_user = User(name="mgju", access_token=access_token)
                session.add(new_user)
                print("➕ 사용자 추가됨")
            await session.commit()
    except Exception:
        print("Try after 1 minute")
        access_token = None

    return access_token

# 주식현재가 시세
# async def get_current_price(stock_no):
#     path = "uapi/domestic-stock/v1/quotations/inquire-price"
#     url = f"{config['STOCK_DOMAIN']}/{path}"

#     async with async_session() as session:
#         session: AsyncSession
#         result = await session.execute(select(User).where(User.name == "mgju"))
#         user = result.scalar_one_or_none()
#         access_token = user.access_token

#     # 헤더 설정
#     headers = {"Content-Type":"application/json", 
#             "authorization": f"Bearer {access_token}",
#             "appKey":config["STOCK_APP_KEY"],
#             "appSecret":config["STOCK_APP_SECRET"],
#             "tr_id":"FHKST01010100"}

#     params = {
#         "fid_cond_mrkt_div_code":"J",
#         "fid_input_iscd": stock_no
#     }

#     # 호출
#     res = requests.get(url, headers=headers, params=params)

#     if res.status_code == 200 and res.json()["rt_cd"] == "0" :
#         return(res.json())
#     # 토큰 만료 시
#     # elif res.status_code == 200 and res.json()["msg_cd"] == "EGW00123" :
#     #     get_auth()
#     #     get_current_price(stock_no)
#     else:
#         print("Error Code : " + str(res.status_code) + " | " + res.text)
#         return None

# async def main():
#     # await get_auth()
#     res = await get_current_price("005930")
#     print(res)


# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())