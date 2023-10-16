# from typing import Any
#
# from app.core.unit_of_work import ABCUnitOfWork
# from app.shortener.repository import ShortenerRepository
# from app.shortener.services import ShortenerServices
# from app.shortener.models import Url
#
#
# class FakeShortenerRepository(ShortenerRepository):
#
#     def __init__(self, *, session) -> None:
#         super().__init__(session=session)
#
#     async def add_entity(self, *, data: dict) -> int:
#         pass
#
#     async def find_by_id(self, *, model_id: int):
#         pass
#
#     async def find_one_or_none(self, **filter_by: Any):
#         pass
#
#
# class FakeShortenerUnitOfWork(ABCUnitOfWork):
#     model = Url
#
#     def __init__(self):
#         self.shortener_repo = FakeShortenerRepository(session=)
#         self.committed = False
#
#     async def commit(self) -> None:
#         self.committed = True
#
#     async def rollback(self) -> None:
#         pass
#
#
# async def test_add_batch():
#     uow = FakeShortenerUnitOfWork()
#     url = 'https://leetcode.com/problemset/all/'
#     await ShortenerServices().create_url(target_url=url, uow=uow)
#
#     res_ = await uow.shortener_repo.find_by_id(model_id=0)
#     print(f'{res_=}')
#     assert uow.shortener_repo.find_by_id(model_id=0) is not None
#     # assert uow.committed
