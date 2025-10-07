import allure

from api.user_api import UserApi
from data.response_status import ResponseStatus
from data.user_data import UserData
from data.error_message import ErrorMessage


class TestLoginEndpoint:

    @allure.title('Логин существующим пользователем')
    @allure.description('Проверка, что можно залогиниться существующим пользователем')
    def test_login_existing_user_user_is_logged_in(self, user_data, register_new_user_authorization_data):
        body = {"email": user_data.get('email'), "password": user_data.get('password')}
        response = UserApi.login_user(body)
        status_code = response.status_code
        success = response.json()['success']
        assert status_code == ResponseStatus.OK and success is True

    @allure.title('Логин несуществующим пользователем')
    @allure.description('Проверка, что нельзя залогиниться несуществующим пользователем')
    def test_login_not_existing_user_error_is_returned(self):
        response = UserApi.login_user(UserData.NOT_EXISTING_USER_CREDENTIALS)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert status_code == ResponseStatus.UNAUTHORIZED and success is False and message == ErrorMessage.INVALID_CREDENTIALS_ERROR_MESSAGE
