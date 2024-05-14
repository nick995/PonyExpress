import os
from sqlmodel import Session, SQLModel, create_engine, select

import json
from datetime import date
import datetime
from uuid import uuid4
from backend.schema import(
    User,
    UserInDB,
    UserCreate,
    ChatInDB,
    MessageInDB,
    ChatUpdate,
    UserUpdate,
    MessageCreate,
    MessageResponse,
    MessageUpdate,
    UserChatLinkInDB,
    MessageInDB
)

def get_db_url():
    if os.environ.get("DB_LOCATION") == "RDS":
        username = os.environ.get("PG_USERNAME")
        password = os.environ.get("PG_PASSWORD")
        endpoint = os.environ.get("PG_ENDPOINT")
        port = os.environ.get("PG_PORT")
        db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"
        echo = False
        connect_args = {}
        return db_url
    else:
        db_url = "sqlite:///backend/pony_express.db"
        echo = True
        connect_args = {"check_same_thread": False}
        return db_url


def get_engine():
    db_url = get_db_url()
    echo = os.environ.get("DB_DEBUG", default="False").lower() in ("true", "1", "t")
    if os.environ.get("DB_LOCATION") == "RDS":
        connect_args = {}
    else:
        connect_args = {"check_same_thread": False}

    return create_engine(db_url, echo=echo, connect_args=connect_args)


engine = get_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
from fastapi import FastAPI, Response, status, HTTPException

class EntityNotFoundException(Exception): 
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class IDAlreadyExisted(Exception): 
    def __init__(self, *, entity_name: str, entity_id: str, type:str):
        self.type = "duplicate_entity"
        self.entity_name = entity_name
        self.entity_id = entity_id

# ---------------users-------------

def get_all_users(session: Session) -> list[UserInDB]:
    return session.exec(select(UserInDB)).all()

def create_user(session: Session ,user_create: UserCreate) -> User:
    """Create a new user in the databse.
        Args:
        user_create (UserCreate): _description_

    Returns:
        UserDB: _description_
    """
    user = User(**user_create.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    

def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve a user from the database.
    
    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    
    user = session.get(UserInDB, user_id)
    if user:
        return user
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def delete_user(session: Session, user_id: int):
    """
    Delete a user from the database.
    
    :param user_id: the id of the user to be deleted
    :raise entityNotFoundEException: if no such user exists
    """
    
    user = get_user_by_id(session, user_id)
    session.delete(user)
    session.commit()

def get_all_chats(session: Session, current_user: User) -> list[ChatInDB]:
    """
    Retrieve all chats from the database that current user is included.
    
    :return: list of chats
    """
    
    # chat = session.exec(select(ChatInDB).where(UserChatLinkInDB.chat_id == ChatInDB.id).where(UserChatLinkInDB.user_id == current_user.id)).all()
    

    print("\n\n\n")
    print(current_user)
    print("\n\n\n")
    
    
    return session.exec(select(ChatInDB).where(UserChatLinkInDB.chat_id == ChatInDB.id).where(UserChatLinkInDB.user_id == current_user.id)).all()

def get_chat_by_id(session: Session, chat_id: int, current_user: User)-> ChatInDB:
    """
    Retrieve a chat from the database.
    
    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    
    # chat = session.exec(select(ChatInDB).where(UserChatLinkInDB.chat_id == ChatInDB.id).where(UserChatLinkInDB.user_id == current_user.id)).all()
    # chat = session.exec(select(UserChatLinkInDB).where((UserChatLinkInDB.chat_id == chat_id) & (UserChatLinkInDB.user_id == current_user.id) )).first()
    user_in_chat_view(session, chat_id, current_user)

    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    if chat:
        return chat
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id= chat_id)


def get_message_by_id(session: Session, message_id: int)-> MessageInDB : 
    """
    Retrieve a chat from the database.
    
    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    message = session.get(MessageInDB, message_id)
    if message:
        return message
    raise EntityNotFoundException(entity_name="message", entity_id= message_id)

def chat_name_update(session: Session,
                     chat_id: int,
                     chat_update: ChatUpdate ) ->ChatInDB :
    """
    Update a chat in the database.
    
    :param chat_id: id of the chat to be updated
    :param chat_update_name: attributes to be updated on the chat
    :return: the updated chat
    """
    
    chat = get_chat_by_id(session, chat_id)
    for attr, value in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat



def user_update(session: Session,
                     user: UserInDB,
                     user_update: UserUpdate ) ->UserInDB :
    """
    Update a chat in the database.
    
    :param chat_id: id of the chat to be updated
    :param chat_update_name: attributes to be updated on the chat
    :return: the updated chat
    """
    
    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def chat_delete(session: Session, chat_id: int):
    """
    Delete a chat in the database.
    
    :parama chat_id: id of the chat to be deleted
    :return: none
    """
    chat = get_chat_by_id(session, chat_id)
    session.delete(chat)
    session.commit()
    
def get_messages_by_chat_id(session: Session, chat_id: int) -> list[MessageInDB]:
    
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    
    if chat:
        return chat.messages
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    
def get_users_by_chat_id(session: Session, chat_id: int) -> list[UserInDB]:
    
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    
    if chat:
        return chat.users
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def create_message(session: Session, 
                   chat_id: int,
                   message_create: MessageCreate,
                   current_user: User ) -> MessageInDB:
    
    is_valid = user_in_chat_view(session, chat_id, current_user)
    existed_chat = session.exec(select(ChatInDB).where(ChatInDB.id ==chat_id)).first()
    if existed_chat:    
        new_message = MessageInDB(
            text=message_create.text,
            user_id=current_user.id,
            chat_id=chat_id,
            user=current_user,
            chat=existed_chat  
        )
        
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        return new_message
    
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id= chat_id)
    
def update_message(session: Session,
                   chat_id: int,
                   message_id: int,
                   message_update: MessageUpdate,
                   current_user: User,
                   )-> MessageResponse:
    
    """
    Update a message in the database.
    
    :param chat_id: id of the chat to be updated
    :param chat_update_name: attributes to be updated on the chat
    :return: the updated chat
    """
    
    #   chat with chat_id must exist, the message with message_id must exis
    get_chat_by_id(session, chat_id, current_user)
    get_message_by_id(session, message_id)
    
    #   to check if user is message owner
    isValid_message = session.exec(select(MessageInDB).where((MessageInDB.user_id == current_user.id) & (MessageInDB.id ==message_id))).first()

    print("\n\n\n")

    if isValid_message:
        for attr, value in message_update.model_dump(exclude_unset=True).items():
            setattr(isValid_message, attr, value)
        session.add(isValid_message)
        session.commit()
        session.refresh(isValid_message)
        return isValid_message
    else:
        
        #If the access token is valid, but the current user is not the 
        # user of the message, the response has HTTP status code 403 
        # and the body has the following format.
        
        raise InvalidUser()
    
def delete_message(session: Session,
                   chat_id: int,
                   message_id: int,
                   current_user: User):
    
    #   to check if chat is exisiting
    chat = get_chat_by_id(session,chat_id, current_user)
    #   to check if emssage is exisiting
    message = get_message_by_id(session, message_id)
    
    isValid_message = session.exec(select(MessageInDB).where((MessageInDB.user_id == current_user.id) & (MessageInDB.id ==message_id))).first()

    if isValid_message:
        session.delete(message)
        session.commit()
    else:
        #If the access token is valid, but the current user is not the 
        # user of the message, the response has HTTP status code 403 
        # and the body has the following format.
        raise InvalidUser()


def user_in_chat_view(session: Session,
                     chat_id: int,
                     current_user: User):
    """To check if user is in the chat or not"""        
    is_valid = session.exec(select(UserChatLinkInDB).where((UserChatLinkInDB.user_id == current_user.id) & (UserChatLinkInDB.chat_id == chat_id))).first()
    
    if is_valid:
        return is_valid
    else:
        raise InvalidView()

def message_owner(session: Session,
                  message_id: int,
                  current_user: User):
    """To check if user is owner of message"""
    return session.exec(select(MessageInDB).
                        where((MessageInDB.user_id == current_user.id) 
                              & (MessageInDB.id == message_id)))

class PermissionException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=403,
            detail={
                "error": error,
                "error_description": description,
            },
        )


class InvalidUser(PermissionException):
    def __init__(self):
        super().__init__(
            error="no_permission",
            description="requires permission to edit message",
        )
        
class InvalidView(PermissionException):
    def __init__(self):
        super().__init__(
            error="no_permission",
            description="requires permission to view chat",
        )