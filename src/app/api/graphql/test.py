import strawberry


@strawberry.type
class TestQuery:
    @strawberry.field
    async def test_api(self, info: strawberry.Info) -> str:
        return "Hello World"
