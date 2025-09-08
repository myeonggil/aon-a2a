# # import collections

# # from typing import Sequence, TypeVar, Iterable, Union

# # T = TypeVar("T", bound=[str])


# # def batch_iter(data: Sequence[T], size: int) -> Iterable[Sequence[T]]:
# #     for i in range(0, len(data), size):
# #         yield data[i:i + size]

# # for data in batch_iter(['1.0', 1.2], 2):
# #     print(data)


# # Card = collections.namedtuple('Card', ['rank', 'suit'])

# # card = Card(rank='2', suit='Spad')

# # class Deck:
# #     def __init__(self, cards: list[Card]):
# #         self.decks = cards

# #     def __len__(self):
# #         return len(self.decks)

# #     def __getitem__(self, position):
# #         return self.decks[position]

# #     def __repr__(self):
# #         return f"Cards"

# # ranks = ['J', 'Q', 'K', 'A']
# # suits = ['Spade', 'Heart', 'A', 'B']
# # cards = [Card(rank=rank, suit=suit) for rank in ranks for suit in suits]
# # deck = Deck(cards=cards)

# from typing import Callable
# from functools import wraps

# from typing import Callable
# from functools import wraps

# import inspect


# class Test:
#     def register_func_tool(self, description: str):
#         def decorator(func: Callable):
#             sig = inspect.signature(func)  # 함수 시그니처 가져오기
#             @wraps(func)
#             def wrapper(*args, **kwargs):
#                 print(f"Description: {description}")
#                 print("Default params:")
#                 for name, param in sig.parameters.items():
#                     if param.default is not inspect.Parameter.empty:
#                         print(f"  {name} = {param.default}")
#                 return func(*args, **kwargs)
#             return wrapper
#         return decorator


# test = Test()

# @test.register_func_tool(description='asd')
# def my_func(x: int = 1, y: int = 2, greet="hello"):
#     # print(f"{greet}, x + y = {x + y}")
#     ...


# # 함수 호출
# # my_func(3, 5, greet="hi")
# # my_func()

arr = [1, 2, 3, 4, 5]

res = filter(lambda x: x == 6, arr)
print(next(res, None))
