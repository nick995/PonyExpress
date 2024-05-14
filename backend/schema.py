from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List





# ------------------------------------- #
#            database models            #
# ------------------------------------- #


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



# ------------------------------------- #
#             request body              #
# ------------------------------------- #


# GET /users returns a list of users sorted by id alongside some metadata. 
# The metadata has the count of users (integer). 
# The response has HTTP status code 200


# POST /users creates a new user. The body of the request adheres to the format:

class UserCreate(BaseModel):
    id: str

class UserDetail(BaseModel):
    type: str
    entity_name: str
    entity_id: str
    
class MessageCreate(BaseModel):
    text: str

class ChatUpdate(BaseModel):
    name: str = None
    text: str
    
class UserUpdate(SQLModel):
    """Request model for updating user in the system."""
    username: str = None
    email: str = None
    
# ------------------------------------- #
#            response models            #
# ------------------------------------- #

class Meta(BaseModel):
    count: int

# ------------------------------------- #
#              User API                 #
# ------------------------------------- #

class User(SQLModel):
    """API response for user"""
    id: int                 
    username: str
    email: str
    created_at: datetime    
    
class UserResponse(BaseModel):
    user: User

class UserResponse2(BaseModel):
    user: UserInDB


class UserCollection(BaseModel):
    meta: Meta
    users: list[User]
# ------------------------------------- #
#              Chat API                 #
# ------------------------------------- #
    
class Chat(SQLModel):
    """API response for chat """
    id: int
    name: str
    owner: User
    created_at: datetime

class ChatResponse(BaseModel):
    chat: Chat

class ChatMeta(BaseModel):
    message_count: int
    user_count: int

class ChatCollection(BaseModel):
    meta: Meta
    chats: list[Chat]

# ------------------------------------- #
#              Message API              #
# ------------------------------------- #
    
class Message(SQLModel):
    """API response for message"""
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime
    
class MessageUpdate(BaseModel):
    """Message Update request body"""
    text: str



class MessageCollection(BaseModel):
    meta: Meta
    messages: list[Message]
    
class MessageResponse(BaseModel):
    message: Message
        
class ChatUpdatedCollection(BaseModel):
    meta: ChatMeta
    chat: Chat
    messages: Optional[list[Message]] = None
    users: Optional[list[User]] = None