from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlmodel import Session
from backend import database as db

from backend.auth import get_current_user


# from backend.schema import(
#     UserInDB,
#     UserCollection,
#     UserCreate,
#     UserResponse,
#     ChatCollection
# )

from backend.schema import *

users_router = APIRouter(prefix="/users", tags=["Users"])



@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=user)


@users_router.put("/me", response_model=UserResponse)
def update_self(
    user_update: UserUpdate2,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session),
):
    """Update current user's username or email."""
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user=user)


@users_router.get("",
description="returns a list of users sorted by id alongside some metadata. The metadata has the count of users (integer)",
response_model=UserCollection)
def get_users(session: Session = Depends(db.get_session)):
    users = db.get_all_users(session)  # This should return a list of UserInDB objects
    sorted_users = sorted(users, key=lambda user: user.id)

    return UserCollection(
        meta={"count": len(sorted_users)},
        users=sorted_users,
    )



# @users_router.post("",
# description="creates a new user given id if id is unique.",  
# response_model=UserResponse)
# def create_user(user_create: UserCreate):
#     """Add a new user to the chat system."""
#     try:
#         user = db.create_user(user_create)
#     except db.DuplicateEntityException as e:
#         raise HTTPException(status_code=422, detail={
#             "type": "duplicate_entity",
#             "entity_name": e.entity_name,
#             "entity_id": e.entity_id
#         })
#     return UserResponse(user=user)


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get a user for a given user id. HTTP404 if id does not exist",
)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    """Get a user for a given id."""

    user = db.get_user_by_id(session, user_id)
    return UserResponse(user=user)



@users_router.get("/{user_id}/chats",
 description="returns a list of chats for a given user id alongside some metadata. The list of chats consists of only those chats where the given user is a participating user and is sorted by name. The metadata contains the count of chats (integer). If id doesnt exist, http404",
 response_model=ChatCollection)
def get_user_chats(user_id: int, session: Session = Depends(db.get_session)):
    """Get a list of chats for a given user id."""
    chats = db.get_chats_for_user(session, user_id)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=chats,
    )
