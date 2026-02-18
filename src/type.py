from typing import TYPE_CHECKING, Any, Self, TypeVar

T = TypeVar("T")


class StrawberryPydanticBase:
    if TYPE_CHECKING:

        @classmethod
        def from_pydantic(cls, model_instance: Any) -> Self: ...  # noqa: ANN401
