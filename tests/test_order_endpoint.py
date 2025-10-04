import allure

from api.order_api import OrderApi
from data.response_status import ResponseStatus
from data.error_message import ErrorMessage
from data.order_data import OrderData
from data.user_data import UserData


class TestOrderEndpoint:

    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description('Проверка, что можно создать заказ авторизованным пользователем')
    def test_create_order_authorized_user_order_is_created(self, user_data, register_new_user_authorization_data):
        response = OrderApi.create_order(register_new_user_authorization_data, OrderData.VALID_INGREDIENTS)
        status_code = response.status_code
        success = response.json()['success']
        owner_name = response.json()['order']['owner']['name']
        owner_email = response.json()['order']['owner']['email']
        assert (status_code == ResponseStatus.OK and success is True and owner_name == user_data['name']
                and owner_email == user_data['email'])

    @allure.title('Создание заказа неавторизованным пользователем')
    @allure.description('Проверка, что можно создать заказ неавторизованным пользователем')
    def test_create_order_not_authorized_user_order_is_created(self):
        response = OrderApi.create_order(UserData.EMPTY_USER_CREDENTIALS, OrderData.VALID_INGREDIENTS)
        status_code = response.status_code
        success = response.json()['success']
        assert status_code == ResponseStatus.OK and success is True and 'number' in response.json()['order']

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Проверка, что нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients_error_is_returned(self, register_new_user_authorization_data):
        response = OrderApi.create_order(register_new_user_authorization_data, OrderData.NO_INGREDIENTS)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert (status_code == ResponseStatus.BAD_REQUEST and success is False and
                message == ErrorMessage.ORDER_WITHOUT_INGREDIENTS_ERROR_MESSAGE)

    @allure.title('Создание заказа с невалидными ингредиентами')
    @allure.description('Проверка, что нельзя создать заказ с невалидными ингредиентами')
    def test_create_order_invalid_ingredients_error_is_returned(self, register_new_user_authorization_data):
        response = OrderApi.create_order(register_new_user_authorization_data, OrderData.INVALID_HASH_INGREDIENTS)
        status_code = response.status_code
        assert status_code == ResponseStatus.INTERNAL_SERVER_ERROR

    @allure.title('Получение заказов пользователя')
    @allure.description('Проверка получения заказов авторизованного пользователя')
    def test_get_orders_authorized_user_orders_are_returned(self, register_new_user_with_order_authorization_data):
        headers, expected_order_id = register_new_user_with_order_authorization_data
        response = OrderApi.get_user_orders(headers)
        status_code = response.status_code
        success = response.json()['success']
        order_id = response.json()['orders'][0]['_id']
        assert status_code == ResponseStatus.OK and success is True and order_id == expected_order_id

    @allure.title('Получение заказов неавторизованного пользователя')
    @allure.description('Проверка, что нельзя получить заказы неавторизованного пользователя')
    def test_get_orders_not_authorized_user_error_is_returned(self):
        response = OrderApi.get_user_orders(UserData.EMPTY_USER_CREDENTIALS)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert status_code == ResponseStatus.UNAUTHORIZED and success is False and message == ErrorMessage.UNAUTHORIZED_ERROR_MESSAGE
