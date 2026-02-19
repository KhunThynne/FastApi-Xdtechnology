from collections.abc import Sequence
from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]) -> None:
        self.session = session
        self.model = model

    # --- CREATE ---
    async def add(self, data_model: T) -> T:
        self.session.add(data_model)
        await self.session.commit()  # type: ignore
        await self.session.refresh(data_model)  # type: ignore
        return data_model

    # --- READ (Get One) ---
    async def get_by_id(self, id: UUID) -> T | None:
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.exec(statement)
        return result.first()

    # --- READ (Get All / List with Pagination) ---
    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    # --- UPDATE ---
    async def update(self, db_obj: T, update_data: dict) -> T:
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    # --- DELETE ---
    async def delete(self, db_obj: T) -> bool:
        await self.session.delete(db_obj)
        await self.session.commit()
        return True

    async def get_and_delete(self, id: UUID) -> UUID | None:
        db_obj = await self.get_by_id(id)
        if db_obj:
            obj_id = db_obj.id
            await self.delete(db_obj)
            return obj_id
        return None
