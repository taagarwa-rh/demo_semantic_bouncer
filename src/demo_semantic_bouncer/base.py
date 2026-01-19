from typing import Any

from pydantic import BaseModel


class Text(BaseModel):
    content: str
    route: str
    metadata: dict[str, Any] = {}


class Collection(BaseModel):
    texts: list[Text]
