from aon_a2a.database.connection import async_session, AsyncSession
from aon_a2a.database.schema import User, Stock
from aon_a2a.agents.stock.models import StockInfo

from datetime import datetime

from sqlalchemy.future import select


class UserRepository:
    def __init__(self):
        self.async_session = async_session

    async def create_user(self):
        async with async_session() as session:
            session: AsyncSession
            new_user = User(
                name="mgju",
                created_at=datetime.now(),
            )
            session.add(new_user)
            await session.commit()
            print("➕ 사용자 추가됨")

    async def get_user(self, name: str = "mgju") -> User:
        async with async_session() as session:
            session: AsyncSession
            result = await session.execute(select(User).where(User.name == "mgju"))
            user = result.scalar_one_or_none()
            return user

    async def update_user(self, access_token: str):
        async with async_session() as session:
            session: AsyncSession
            result = await session.execute(select(User).where(User.name == "mgju"))
            user = result.scalar_one_or_none()
            # 있으면 업데이트
            user.access_token = access_token
            user.updated_at = datetime.now()
            await session.commit()
            print("➕ 토큰 갱신")

    async def delete_user(self):
        pass


class StockRepository:
    def __init__(self):
        self.async_session = async_session

    async def create_stock(self, stock_infos: list[StockInfo]):
        async with async_session() as session:
            session: AsyncSession
            for stock_info in stock_infos:
                new_stock = Stock(
                    stock_code=stock_info.stock_code,
                    stock_name=stock_info.stock_name,
                    market_division=stock_info.market_division
                )
                session.add(new_stock)
            await session.commit()
            print("➕ 주식 추가됨")
    
    async def get_stock_by_code(self, stock_code: str) -> Stock:
        async with async_session() as session:
            session: AsyncSession
            result = await session.execute(select(Stock).where(Stock.stock_code == stock_code))
            stock = result.scalar_one_or_none()
            return stock

    async def get_stock_by_name(self, stock_name: str) -> Stock:
        async with async_session() as session:
            session: AsyncSession
            result = await session.execute(select(Stock).where(Stock.stock_name == stock_name))
            stock = result.scalar_one_or_none()
            return stock

    # async def update_stock(self, stock_code: str):
    #     async with async_session() as session:
    #         session: AsyncSession
    #         result = await session.execute(select(User).where(User.name == "mgju"))
    #         user = result.scalar_one_or_none()
    #         # 있으면 업데이트
    #         user.access_token = access_token
    #         user.updated_at = datetime.now()
    #         await session.commit()
    #         print("➕ 토큰 갱신")

    # async def delete_stock(self):
    #     pass
