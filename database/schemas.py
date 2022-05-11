from pydantic import BaseModel
from typing import Optional

class DeviseBase(BaseModel):
    dev_type: str
    dev_id: str
    endpoint: Optional[int]
