from datetime import date, datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel


#Database Models------------------

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )

class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")


class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")



# #Request Models---------------------------
class UserCreate(BaseModel):
   id: str


class UserDetails(BaseModel):
   type: str
   entity_name: str
   entity_id: str
  
class MessageCreate(BaseModel):
   text: str
  
class ChatUpdate(BaseModel):
   name: str = None
  
class UserUpdate(SQLModel):
   username: str = None
   email: str = None

class UserUpdate2(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


#Response Models------------------------------

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

class ChatMetadata(BaseModel):
    message_count: int
    user_count: int

class User(SQLModel):
    """Represents an API response for a user."""
    id: int
    username: str
    email: str
    created_at: datetime

class Chat(SQLModel):
    """ Represents an API response for an chat."""

    id: int
    name: str
    owner: User
    created_at: datetime


class Message(SQLModel):
    """Represents an API response for a user."""
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime

class ChatResponse(BaseModel):
    """Represents an API response for an animal."""

    chat: Chat

class ChatResponse2(BaseModel):
    meta: ChatMetadata
    chat: Chat
    messages: Optional[List[Message]] = None
    users: Optional[List[User]] = None
class UserResponse(BaseModel):
    """Represents an API response for an animal."""

    user: User

class MessageResponse(BaseModel):
    """Represents an API response for an animal."""

    message: Message
class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""

    meta: Metadata
    chats: List[Chat]


class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: List[User]

class MessageCollection(BaseModel):
    meta: Metadata
    messages: List[Message]