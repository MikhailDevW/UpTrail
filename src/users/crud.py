from src.base import CRUDBase
from src.users.models import CustomUser


class UserCrud(CRUDBase):
    pass


user_crud = UserCrud(CustomUser)
