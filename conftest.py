import pytest
from faker import Faker

from api.user_api import UserApi
from api.order_api import OrderApi
from data.order_data import OrderData

@pytest.fixture(scope='function')
def user_data():
    faker = Faker()
    user_data = {
        "email": f'{faker.email()}tstzim',
        "password": f'{faker.password(length=7, special_chars=False, upper_case=False, digits=False)}',
        "name": f'{faker.name()}'
    }
    return user_data

@pytest.fixture(scope='function')
def new_user_data_for_update():
    faker = Faker()
    new_user_data = {
        "email": f'{faker.email()}tstzim',
        "name": f'{faker.name()}'
    }
    return new_user_data

@pytest.fixture(scope='function')
def register_new_user_authorization_data(user_data):
    register_response = UserApi.register_new_user(user_data)
    token = register_response.json()['accessToken']
    yield {"Authorization": token}
    UserApi.delete_user(token)

@pytest.fixture(scope='function')
def register_new_user_with_order_authorization_data(user_data):
    register_response = UserApi.register_new_user(user_data)
    token = {"Authorization": register_response.json()['accessToken']}
    response = OrderApi.create_order(token, OrderData.VALID_INGREDIENTS)
    order_id = response.json()['order']['_id']
    yield token, order_id
    UserApi.delete_user(register_response.json()['accessToken'])


@pytest.fixture(scope='function')
def register_new_user(user_data):
    register_response = UserApi.register_new_user(user_data)
    token = register_response.json()['accessToken']
    yield register_response
    UserApi.delete_user(token)
