import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db
from backend import auth
from backend.schema import UserCreate, ChatCreate

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def logged_in_client(session, user_fixture):
    def _get_session_override():
        return session

    def _get_current_user_override():
        return user_fixture(username="juniper")

    app.dependency_overrides[db.get_session] = _get_session_override
    app.dependency_overrides[auth.get_current_user] = _get_current_user_override

    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def user_fixture(session):
    def _build_user(
        username: str = "juniper",
        email: str = "juniper@cool.email",
        password: str = "password",
    ) -> db.UserInDB:
        user_create = UserCreate(username=username, email=email, password=password)
        return db.create_user(session, user_create)

    return _build_user

@pytest.fixture
def chat_fixture(session, user_fixture):
    def _build_chat(
        name: str = "Test Chat",
        owner_id: int = None,
    ) -> db.ChatInDB:
        if owner_id is None:
            owner = user_fixture()
            owner_id = owner.id
        chat_create = ChatCreate(name=name, owner_id=owner_id)
        return db.create_chat(session, chat_create)

    return _build_chat
