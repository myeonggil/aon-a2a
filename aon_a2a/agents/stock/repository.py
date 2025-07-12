from aon_a2a.database.connection import async_session, AsyncSession
from aon_a2a.database.schema import User

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
