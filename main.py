import strawberry


@strawberry.type
class Prompt:
    query: str
    answer: str
    code: str


@strawberry.type
class Query:
    @strawberry.field
    def prompt(self) -> Prompt:
        return Prompt(query="Prompt", answer="Answer", code="Code")


schema = strawberry.Schema(query=Query)
