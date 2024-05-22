from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from backend.auth import get_current_user

from sqlmodel import Session

# from backend.schema import (
#     ChatCollection,
#     ChatCreate,
#     ChatInDB,
#     ChatUpdate,
#     ChatResponse,
#     MessageCollection,
#     MessageInDB,
#     UserCollection
# )

from backend.schema import *

from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", 
description="returns a list of chats sorted by name alongside some metadata. The metadata has the count of chats (integer)",
response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    chats = db.get_all_chats(session)  # This should return a list of ChatInDB objects
    sorted_chats = sorted(chats, key=lambda chat: chat.name)

    return ChatCollection(
        meta={"count": len(sorted_chats)},
        chats=sorted_chats,
    )


@chats_router.get(
    "/{chat_id}",
    response_model=ChatResponse2,
    description="Get a chat by its id, optionally including messages and users.",
    response_model_exclude_none = True
)
def get_chat(
    chat_id: str,
    include: List[str] = Query(default=[]),
    session: Session = Depends(db.get_session)
):
    chat = db.get_chat_by_id(session, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    
    response = ChatResponse2(
        meta=ChatMetadata(
            message_count=len(chat.messages),
            user_count=len(chat.users)
        ),
        chat=chat,
        messages=chat.messages if "messages"in include else None,
        users=chat.users if "users" in include else None,
    )

    return response



@chats_router.put("/{chat_id}", 
description="updates a chat for a given id. The body for the request has the info to update",
response_model=ChatResponse)
def update_chat(
    chat_id: int, 
    chat_update: ChatUpdate,
    session: Session = Depends(db.get_session)
):
    """Update a chat for a given id."""

    updated_chat = db.update_chat(session, chat_id, chat_update)
    return ChatResponse(chat=updated_chat)


# @chats_router.delete(
#     "/{chat_id}",
#     status_code=204,
#     response_model=None,
#     description="Deletes a chat for a given id. If a chat with the id exists, the chat is removed from the database, and the response has the HTTP status code of 204 and has no content. If the id provided does not correspond to an existing chat, the response has the HTTP status code 404."
# )
# def delete_chat(chat_id: str) -> None:
#     db.delete_chat(chat_id)


@chats_router.get("/{chat_id}/messages",
description="returns a list of messages for a given chat id alongside some metadata. The metadata contains the count of messages (integer) and the list of messages is sorted by its created_at datetime. If a chat with the id doesn't exist, HTTP404",
response_model=MessageCollection)
def get_chat_messages(chat_id: int, session: Session = Depends(db.get_session)):
    messages = db.get_chat_messages_by_chat_id(session, chat_id)
    sorted_messages = sorted(messages, key=lambda msg: msg.created_at)

    return MessageCollection(
        meta={"count": len(sorted_messages)},
        messages=sorted_messages
    )


@chats_router.get("/{chat_id}/users",
description="returns a list of users for a given chat id alongside some metadata. The list of users consists of only those users participating in the corresponding chat, sorted by id. The metadata contains the count of users (integer). If a chat with the id doesnt exist, http 404", 
response_model=UserCollection)
def get_chat_users(chat_id: int, session: Session = Depends(db.get_session)):
    """Get a list of users for a given chat id."""
    users = db.get_users_for_chat(session, chat_id)
    return UserCollection(
        meta={"count": len(users)},
        users=users,
    )

@chats_router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=201)
def create_chat_message(
    chat_id: str,
    message_create: MessageCreate,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session),
):
    message = db.create_message(session, chat_id, user.id, message_create)
    return MessageResponse(message=message)
