from pydantic import BaseModel, ConfigDict

class TagBase(BaseModel):
    name: str
    color: str | None = None

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)