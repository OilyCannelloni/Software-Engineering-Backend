import pathlib
import uuid
from models.models import *
from core.server import server
from main import app
from fastapi.testclient import TestClient


def test_pool_CRUD():
    q1 = Question(
        text="Question 1",
        type=QuestionType.MULTIPLE_CHOICE,
        options=[
            QuestionOption(text="opt 1"),
            QuestionOption(text="opt 2", is_optional=True),
        ],
    )
    q2 = Question(
        text="Question 2",
        type=QuestionType.TEXTBOX,
        textbox=QuestionTextbox(initial_value="init_val"),
    )
    poll = Poll(
        title="Test Poll",
        description="Testing JSON serialization",
        questions={"q1": q1, "q2": q2},
    )

    test_pool_name = str(uuid.uuid4())
    test_pool_name2 = str(uuid.uuid4())

    # Create
    client = TestClient(app)
    response = client.post(f"/poll/{test_pool_name}/save", json=poll.dict())
    assert response.status_code == 200
    response = client.post(f"/poll/{test_pool_name2}/save", json=poll.dict())
    assert response.status_code == 200

    # Read
    response = client.get("/polls")
    assert test_pool_name in response.text
    assert test_pool_name2 in response.text

    response_text = client.get(f"/poll/{test_pool_name}/load").text
    pool_from_server = Poll(**json.loads(response_text))

    assert pool_from_server.title == "Test Poll"
    assert pool_from_server.description == "Testing JSON serialization"
    assert pool_from_server.questions["q1"].textbox.is_visible == False
    assert pool_from_server.questions["q1"].type == QuestionType.MULTIPLE_CHOICE
    assert len(pool_from_server.questions) == 2
    assert pool_from_server.questions["q1"].options[0].text == "opt 1"
    assert len(pool_from_server.questions["q1"].options) == 2
    assert len(pool_from_server.questions["q2"].options) == 0

    # Update
    poll.title = "Updated Test Poll"
    response = client.post(f"/poll/{test_pool_name}/save", json=poll.dict())
    assert response.status_code == 200
    response_text = client.get(f"/poll/{test_pool_name}/load").text
    pool_from_server = Poll(**json.loads(response_text))
    assert pool_from_server.title == "Updated Test Poll"

    # Delete
    response = client.delete(f"/poll/{test_pool_name}")
    assert response.status_code == 200
    response = client.delete(f"/poll/{test_pool_name2}")
    assert response.status_code == 200
    response = client.get("/polls")
    assert response.status_code == 200
    assert test_pool_name not in response.text
    assert test_pool_name2 not in response.text
