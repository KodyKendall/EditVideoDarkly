import os

from sqlalchemy import func
import json
from datetime import date, datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select

# from backend.schema import (
#     ChatCollection,
#     ChatCreate,
#     ChatInDB,
#     ChatUpdate,
#     ChatResponse,
#     MessageInDB,
#     MessageCollection,
#     UserInDB,
#     UserCollection,
#     UserCreate
# )

from backend.schema import *

# with open("backend/fake_db.json", "r") as f:
#     DB = json.load(f)

def get_db_url():
    loc = os.environ.get("DB_LOCATION")
    if loc == "efs":
        return "sqlite:////mnt/efs/buddy_system.db"
    if loc == "rds":
        username = os.environ.get("PG_USERNAME")
        password = os.environ.get("PG_PASSWORD")
        endpoint = os.environ.get("PG_ENDPOINT")
        port = os.environ.get("PG_PORT")
        return f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"

    return "sqlite:///backend/buddy_system.db"


def get_engine():
    db_url = get_db_url()
    echo = os.environ.get("DB_DEBUG", default="False").lower() in ("true", "1", "t")
    if os.environ.get("DB_LOCATION") == "rds":
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


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


class DuplicateEntityException(Exception):
    def __init__(self, entity_name, entity_id):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with ID {entity_id} already exists")


#   -------- chats --------   #


def get_all_chats(session: Session) -> ChatCollection:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """
    return session.exec(select(ChatInDB)).all()


# def create_animal(animal_create: AnimalCreate) -> AnimalInDB:
#     """
#     Create a new animal in the database.

#     :param animal_create: attributes of the animal to be created
#     :return: the newly created animal
#     """

#     animal = AnimalInDB(
#         id=uuid4().hex,
#         intake_date=date.today(),
#         **animal_create.model_dump(),
#     )
#     DB["animals"][animal.id] = animal.model_dump()
#     return animal


def get_chat_by_id(session: Session, chat_id: str) -> ChatResponse:
    """
    Retrieve a chat from the database.

    :param session: SQLAlchemy session
    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    :raises EntityNotFoundException: if no such chat id exists
    """
    chat = session.get(ChatInDB, chat_id)
    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    return chat



def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update a chat in the database.

    :param session: SQLAlchemy session
    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated chat
    :raises EntityNotFoundException: if no such chat id exists
    """

    chat = get_chat_by_id(session, chat_id)
    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

    for attr, value in chat_update.dict(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat


# def delete_chat(chat_id: str):
#     """
#     Delete a chat from the database.

#     :param chat_id: the id of the chat to be deleted
#     :raises EntityNotFoundException: if no such chat exists
#     """

#     chat = get_chat_by_id(chat_id)
#     del DB["chats"][chat.id]


def get_chat_messages_by_chat_id(session: Session, chat_id: int) -> list[Message]:
    """
    Retrieve chat messages from the database.

    :param session: SQLAlchemy session
    :param chat_id: id of the chat whose messages are to be retrieved
    :return: the retrieved messages, sorted by created_at
    :raises EntityNotFoundException: if no such chat id exists
    """
    chat = session.get(ChatInDB, chat_id)
    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

    messages = (
        session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id).order_by(MessageInDB.created_at)).all()
    )

    return messages



# #   -------- users --------   #


def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :param session: SQLAlchemy session
    :return: ordered list of users
    """
    return session.exec(select(UserInDB)).all()



# def create_user(user_create: UserCreate) -> UserInDB:
#     """
#     Create a new user in the database.

#     :param user_create: attributes of the user to be created
#     :return: the newly created user
#     """

#     if user_create.id in DB["users"]:
#         raise DuplicateEntityException("User", user_create.id)

#     user = UserInDB(
#         id=user_create.id,
#         created_at=datetime.now(),
#     )
#     DB["users"][user.id] = user.model_dump()
#     return user


def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve a user from the database.

    :param session: SQLAlchemy session
    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """

    user = session.get(UserInDB, user_id)
    if user is None:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)

    return user



def get_chats_for_user(session: Session, user_id: int) -> list[ChatInDB]:
    """
    Retrieve chats for a given user from the database.

    :param session: SQLAlchemy session
    :param user_id: ID of the user whose chats are to be retrieved
    :return: list of chats the user is part of
    :raises EntityNotFoundException: if no such user id exists
    """
    user = session.get(UserInDB, user_id)
    if user is None:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)

    user_chats = (session.exec(select(ChatInDB).join(UserChatLinkInDB).where(UserChatLinkInDB.user_id == user_id)).all())
    return sorted(user_chats, key=lambda chat: chat.name)



def get_users_for_chat(session: Session, chat_id: int) -> list[UserInDB]:
    """
    Retrieve users for a given chat from the database.

    :param session: SQLAlchemy session
    :param chat_id: ID of the chat
    :return: list of users in the chat
    :raises EntityNotFoundException: if no such chat id exists
    """
    chat = session.get(ChatInDB, chat_id)
    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

    users = (
        session.exec(select(UserInDB).join(UserChatLinkInDB).where(UserChatLinkInDB.chat_id == chat_id)).all()
    )
    return users



# def update_user(user_id: str, user_update: UserUpdate) -> UserInDB:
#     """
#     Update an user in the database.

#     :param user_id: id of the user to be updated
#     :param user_update: attributes to be updated on the user
#     :return: the updated user
#     """

#     user = get_user_by_id(user_id)
#     for key, value in user_update.update_attributes().items():
#         setattr(user, key, value)
#     return user


# def delete_user(user_id: str):
#     """
#     Delete an user from the database.

#     :param user_id: the id of the user to be deleted
#     """

#     user = get_user_by_id(user_id)
#     del DB["users"][user.id]


#------Message
def create_message(session: Session, chat_id: str, user_id: str, message_create: MessageCreate) -> MessageInDB:
    chat = session.get(ChatInDB, chat_id)
    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

    message = MessageInDB(
        text=message_create.text,
        chat_id=chat_id,
        user_id=user_id,
        created_at=datetime.now(),
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

