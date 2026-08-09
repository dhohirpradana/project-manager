from pydantic import BaseModel, ConfigDict

class DependencyCreate(BaseModel):
    task_id: int
    depends_on_task_id: int

class DependencyOut(BaseModel):
    id: int
    task_id: int
    depends_on_task_id: int
    model_config = ConfigDict(from_attributes=True)