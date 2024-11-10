from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_read_all_athenticated(test_todo):
    response = client.get("/todos/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to Code!', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5, 'owner_id': 1}]

def test_read_one_athenticated(test_todo):
    response = client.get("/todos/todo/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Learn to Code!', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5, 'owner_id': 1}

def test_read_one_authenticated_not_found():
    response = client.get('/todos/todo/999')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not Found.'}

def test_create_todo(test_todo):
    request_data = {
        'title' : 'New Todo!',
        'description' : 'New Todo Description',
        'priority' : 5,
        'complete' : False
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    update_data = {
        "title" : 'Learn to Code!',
        "description" : 'Need to learn everymonth!',
        "priority" : 5,
        "complete" : True,
        "owner_id" : 1
    }

    response = client.put('/todos/todo/1', json=update_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert update_data.get('complete') == model.complete
    assert update_data.get('description') == model.description

def test_update_todo_not_found(test_todo):
    update_data = {
        "title" : 'Learn to Code!',
        "description" : 'Need to learn everymonth!',
        "priority" : 5,
        "complete" : True,
        "owner_id" : 1
    }

    response = client.put('/todos/todo/999', json=update_data)
    assert response.status_code == 404

    assert response.json() == {'detail': 'Todo Not Found!'}

def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')

    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None

def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo Not Found!'}