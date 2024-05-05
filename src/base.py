from http import HTTPStatus

from fastapi import HTTPException

from src.database import async_session


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_object_or_404(
        self,
        object_id: int,
        session,
    ):
        """
        Возвращает обьект модели по его id
        или 404 в случае отсутствия.
        """
        async with async_session() as session:
            object = await session.get(self.model, object_id)
        if object is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Объект {self.model.__tablename__} не найден.",
            )
        return object
