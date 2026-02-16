from sqlmodel import Field, SQLModel


class UserSettings(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
