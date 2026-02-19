from sqlmodel import Session

from models.licenses_schema import LicensesTable

from .shared import BaseRepository


class LicensesRepository(BaseRepository[LicensesTable]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, LicensesTable)
