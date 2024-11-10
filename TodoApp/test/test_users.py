from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "marouan_08"
    assert response.json()['email'] == "marouan@gmail.com"
    assert response.json()['first_name'] == "Marouan"
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "(+90) 536-233-97-40"



def test_change_password_success(test_user):
    response = client.put("/user/change_password", json={"current_password" : "12345", "new_password" : "54321"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put("/user/change_password", json={"current_password" : "42345", "new_password" : "54321"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail' : "Current password is incorrect!!!"}


def test_change_phone_number_success(test_user):
    response = client.put('/user/update_phone_number/0666280030')
    assert response.status_code == status.HTTP_204_NO_CONTENT