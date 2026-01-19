from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreateDTO(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
