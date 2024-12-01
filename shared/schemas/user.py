from pydantic import BaseModel
from typing import Optional

class User_Login(BaseModel):
    username: str
    password: str

class User_Create(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    f_name: str
    l_name: str