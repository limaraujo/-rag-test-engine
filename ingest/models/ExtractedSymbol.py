from pydantic import BaseModel


class ExtractedSymbol(BaseModel):

    symbol_type: str

    name: str

    class_name: str | None

    file_path: str

    source_code: str

    imports: list[str]

    dependencies: list[str]

    exceptions: list[str]

    decorators: list[str]

    docstring: str | None

    branches: int

    edge_cases: list[str]