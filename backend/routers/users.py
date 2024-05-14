from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlmodel import Session

#   before we add some routes, we need to define some data models.
#   entities.py

from backend import database as db
from backend.schema import (
    UserCollection,
    UserResponse,
    User,
    ChatCollection,
    UserInDB,    
    UserUpdate,
    
)
from backend.auth import get_current_user


#   define router,
users_router = APIRouter(prefix="/users", tags=["Users"])

#   under the tag "Users" there are 3 routes.

# GET /users
#   GET /users returns a list of users sorted by id alongside some metadata. 
#   The metadata has the count of users (integer). The response has HTTP status 
#   code 200 and adheres to the following format:
@users_router.get("",
                  description = "return a list of users",
                  response_model = UserCollection)
def get_users(
        sort: Literal["id", "created_at"] = "id",
        session: Session = Depends(db.get_session)):
    
    sort_key = lambda user: getattr(user, sort)

    users = db.get_all_users(session)
    return  UserCollection(
        meta={"count": len(users)},
        users = sorted(users, key=sort_key)
    )

#The POST /users route should be deleted. This will be replaced by the POST /auth/registration route below.
# @users_router.post("", 
#                    description = "users creates a new user",
#                    response_model = UserResponse)
# def create_user(user_create: UserCreate):
#     return UserResponse(user = db.create_user(user_create))


"""
    GET /users/me returns the current user. 
    It requires a valid bearer token. 
    If the token is valid, the response has HTTP status code 200 and 
    the response adheres to the format:
"""
@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=user)


# GET /users/{user_id}
@users_router.get("/{user_id}", 
                  response_model = UserResponse, 
                  description = "return users by given id")
def get_user(user_id: int, session: Session = Depends(db.get_session)):

    return UserResponse(
        user=db.get_user_by_id(session, user_id),
    )

# GET /users/{user_id}/chats
@users_router.get("/{user_id}/chats",
                  response_model = ChatCollection,
                  description = "return a list of chats for a given user id",
                  )
def get_user_chats(user_id: int,
                   sort: Literal["id", "name", "created_at"] = "name",
                   session: Session = Depends(db.get_session)):
    
    user = db.get_user_by_id(session, user_id)
    
    chats = user.chats
    return  ChatCollection(
        meta={"count": len(chats)},
        chats = sorted(chats, key=lambda chat: chat.name),
        
    )   

# {
#   "username": "new_username",
#   "email": "new_email@example.com"
# }

@users_router.put("/me", 
                  response_model=UserResponse,
                  description="update chat")
def update_user(
    user_update: UserUpdate,
    user: UserInDB = Depends(get_current_user), 
    session: Session = Depends(db.get_session),
):

    updated_user = db.user_update(session, user, user_update)
    return UserResponse(user=updated_user)



# @users_router.get("/me", response_model=UserResponse)
# def get_self(user: UserInDB = Depends(get_current_user)):
#     """Get current user."""
#     return UserResponse(user=user)