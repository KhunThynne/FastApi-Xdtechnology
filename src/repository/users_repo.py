from sqlmodel import Session

from models.users_schema import UsersTable

from .shared import BaseRepository


class UserRepository(BaseRepository[UsersTable]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, UsersTable)
