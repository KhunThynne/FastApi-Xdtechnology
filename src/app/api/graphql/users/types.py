from dataclasses import dataclass

import strawberry


@strawberry.type
@dataclass
class UserType:
    id: int
    username: str
    email: str
