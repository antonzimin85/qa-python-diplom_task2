import allure
import pytest

from api.user_api import UserApi
from data.response_status import ResponseStatus
from data.error_message import ErrorMessage
from data.user_data import UserData


class TestRegisterEndpoint:

    @allure.title('Регистрация нового пользователя')
    @allure.description('Проверка, что новый пользователь успешно зарегистрирован')
    def test_user_registration_new_user_user_is_registered(self, register_new_user):
        status_code = register_new_user.status_code
        success = register_new_user.json()['success']
        assert status_code == ResponseStatus.OK and success is True

    @allure.title('Регистрация существующего пользователя')
    @allure.description('Проверка, что нельзя зарегистрировать повторно существующего пользователя')
    def test_user_registration_existing_user_error_is_returned(self, user_data, register_new_user):
        response = UserApi.register_new_user(user_data)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert (status_code == ResponseStatus.FORBIDDEN and success is False and
                message == ErrorMessage.USER_EXISTS_ERROR_MESSAGE)

    @allure.title('Регистрация пользователя без обязательного поля')
    @allure.description('Проверка, что нельзя зарегистрировать пользователя без обязательного поля')
    @pytest.mark.parametrize('user_data', UserData.USERS_WITHOUT_MANDATORY_FIELD)
    def test_user_registration_without_mandatory_field_error_is_returned(self, user_data):
        response = UserApi.register_new_user(user_data)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert (status_code == ResponseStatus.FORBIDDEN and success is False and
                message == ErrorMessage.REQUIRED_FIELDS_MISSING_ERROR_MESSAGE)
