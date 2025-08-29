from dataclasses import dataclass

from msgspec import Struct


class User(Struct):
    user_id: int
    name: str
    expired_at: int

# Request login
class AuthRequest(Struct):
    email: str

class AuthResponse(Struct):
    token: str


# Request chat
class ChatResponse(Struct):
    content: str
