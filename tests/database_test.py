from backend.schema import *


def test_relationships(session):
    # Create a user
    reese = UserInDB(
        username="reese",
        email="reese@cool.email",
        hashed_password="hashed___password",
    )
    # Create a chat
    terminators = ChatInDB(
        name="Terminators",
        owner=reese,
    )
    # Create a message in the chat authored by the user
    message = MessageInDB(
        text="I'll be back.",
        user=reese,
        chat=terminators,
    )
    session.add(reese)
    session.add(terminators)
    session.add(message)
    session.commit()
    session.refresh(reese)
    session.refresh(terminators)
    session.refresh(message)

    # Check relationships
    assert terminators.owner == reese
    assert reese in terminators.users
    assert message in terminators.messages
    assert message.user == reese
