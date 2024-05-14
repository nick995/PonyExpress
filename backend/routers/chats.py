from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session
from typing import Optional
from typing import Annotated

from backend.schema import (
    ChatCollection,
    ChatResponse,
    ChatUpdate,
    MessageCollection,
    UserCollection,
    MessageCreate,
    MessageResponse,
    MessageUpdate,
    UserInDB,
    ChatMeta,
    ChatUpdatedCollection,
)
from typing import Literal
from backend import database as db
from backend.auth import get_current_user

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


# GET /chats
@chats_router.get("",
                response_model = ChatCollection,
                description= " returns a list of chats sorted by name alongside some metadata.", 
)
def get_chats(
            sort: Literal["id", "name", "user_ids", "owner_id", "created_at"] = "name",
            session: Session = Depends(db.get_session),
            current_user: UserInDB = Depends(get_current_user), 
            ):
    
    sort_key = lambda user: getattr(user, sort)
    chats = db.get_all_chats(session, current_user)
    
    return ChatCollection(
        meta= {"count": len(chats)},
        chats = sorted(chats, key=sort_key)
    )

#   The GET /chats/{chat_id} will be enhanced with new functionality, see below.

@chats_router.get("/{chat_id}", 
                  response_model = ChatUpdatedCollection,
                  description = "return chat information message_count & user_count",
                  response_model_exclude_none= True)
def get_chat_by_id(chat_id: int,
                   current_user: UserInDB = Depends(get_current_user), 
                   include: Annotated[list[str] | None, Query()] = None,
                   session: Session = Depends(db.get_session)):
    
    chat = db.get_chat_by_id(session, chat_id, current_user)
    print(include)
    if include:
        
        if "messages" in include and "users" in include:
            users = db.get_users_by_chat_id(session, chat_id)
            messages = db.get_messages_by_chat_id(session, chat_id)

            return ChatUpdatedCollection(
                meta = ChatMeta(
                    message_count = len(chat.messages),
                    user_count = len(chat.users),
                    ),
                chat = chat,
                users = users,
                messages = messages,
            )
        
        elif "messages" in include:
            messages = db.get_messages_by_chat_id(session, chat_id)
            return ChatUpdatedCollection(
                meta = ChatMeta(
                    message_count = len(chat.messages),
                    user_count = len(chat.users),
                    ),
                chat = chat,
                messages = messages,
            )
        elif "users" in include:
            users = db.get_users_by_chat_id(session, chat_id)
            return ChatUpdatedCollection(
                meta = ChatMeta(
                    message_count = len(chat.messages),
                    user_count = len(chat.users),
                    ),
                chat = chat,
                users = users,
            )
        else:
            pass
    
    return ChatUpdatedCollection(
        meta = ChatMeta(
            message_count = len(chat.messages),
            user_count = len(chat.users),
            ),
        chat = chat,

    )

# PUT /chats/{chat_id} updates a chat for a given id. 
# The body for the request adheres to the format:

@chats_router.put("/{chat_id}", 
                  response_model = ChatResponse,
                  description = "update chat" )
def update_chat(chat_id: int, 
                chat_update: ChatUpdate,
                session: Session = Depends(db.get_session),):

    updated_chat = db.chat_name_update(session, chat_id, chat_update)
    return ChatResponse(chat = updated_chat)


    """return all of messages

    Returns:
        MessageCollection: count and messages
    """
@chats_router.get("/{chat_id}/messages", 
                  response_model = MessageCollection,
                  description = "get list of chats by given chat_id" 
)
def get_messages(
            chat_id: int,
            current_user: UserInDB = Depends(get_current_user), 
            sort: Literal["id", "text", "chat_id"  , "created_at"] = "id",
            session: Session = Depends(db.get_session),):
    
    sort_key = lambda messages: getattr(messages, sort)
    chat = db.get_chat_by_id(session, chat_id, current_user)

    messages = chat.messages

    return  MessageCollection(
        meta={"count": len(messages)},
        messages = sorted(messages, key=sort_key)
    )
    
    
@chats_router.get("/{chat_id}/users", 
                  response_model =UserCollection,
                  description = "return list of users by given chat id" )
def get_all_users_by_chat_id(
    chat_id: int,
    current_user: UserInDB = Depends(get_current_user),
    sort: Literal["id", "created_at"] = "id",
    session: Session = Depends(db.get_session)
):  
    # get chat -> get user_ids -> return users
    chat = db.get_chat_by_id(session, chat_id, current_user)
    sort_key = lambda user: getattr(user, sort)
    users = chat.users
    
    return UserCollection(
        meta= {"count": len(users)},
        users = sorted(users, key=sort_key)
    )
    
@chats_router.post("/{chat_id}/messages",
                   response_model = MessageResponse ,
                   status_code = 201,)
def create_message(
        chat_id: int,
        message_create: MessageCreate,
        current_user: UserInDB = Depends(get_current_user), 
        session: Session = Depends(db.get_session)):
    return MessageResponse(message = db.create_message(session, chat_id , message_create, current_user))

@chats_router.put("/{chat_id}/messages/{message_id}",
                  response_model= MessageResponse,
                  status_code=200,
                  description= "update message")
def edit_message(message_id: int,
                 chat_id: int,
                 message_update: MessageUpdate,
                 current_User: UserInDB = Depends(get_current_user), 
                 session: Session = Depends(db.get_session)):
    updated_message = db.update_message(session, chat_id ,message_id, message_update, current_User)
    return MessageResponse(message = updated_message)


@chats_router.delete("/{chat_id}/messages/{message_id}",
                  status_code=204,
                  description= "delete message")
def delete_message(message_id: int,
                   chat_id: int,
                   current_user: UserInDB = Depends(get_current_user),
                   session: Session = Depends(db.get_session)) -> None:
    delete_message = db.delete_message(session, chat_id, message_id, current_user)


