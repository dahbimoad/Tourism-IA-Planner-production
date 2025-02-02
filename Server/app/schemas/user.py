from pydantic import BaseModel, EmailStr

# Schema for user signup
class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr  # Validate that the email is in proper format
    password: str

    class Config:
        orm_mode = True

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr  # Validate email format
    password: str

    class Config:
        orm_mode = True

# Schema for user output (excluding password)
class UserOut(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr  # Return email in proper format

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    email: EmailStr | None = None

    class Config:
        from_attributes = True