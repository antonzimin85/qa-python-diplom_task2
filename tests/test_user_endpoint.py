import allure
import pytest

from api.user_api import UserApi
from conftest import new_user_data_for_update
from data.response_status import ResponseStatus
from data.error_message import ErrorMessage
from data.user_data import UserData


class TestUserEndpoint:

    @allure.title('Изменение данных авторизованного пользователя')
    @allure.description('Проверка, что можно изменить данные авторизованного пользователя')
    @pytest.mark.parametrize('new_user_data,updated_field', UserData.UPDATE_USER_DATA)
    def test_update_user_data_authorized_user_user_data_is_updated(self, register_new_user_authorization_data, new_user_data, updated_field):
        response = UserApi.update_user_data(register_new_user_authorization_data, new_user_data)
        status_code = response.status_code
        success = response.json()['success']
        updated_user_data = response.json()['user'][updated_field]
        assert status_code == ResponseStatus.OK and success is True and updated_user_data == new_user_data[updated_field]

    @allure.title('Изменение данных неавторизованным пользователем')
    @allure.description('Проверка, что нельзя изменить данные не авторизованного пользователя')
    def test_update_user_data_not_authorized_user_error_is_returned(self, new_user_data_for_update):
        response = UserApi.update_user_data(UserData.EMPTY_USER_CREDENTIALS, new_user_data_for_update)
        status_code = response.status_code
        success = response.json()['success']
        message = response.json()['message']
        assert (status_code == ResponseStatus.UNAUTHORIZED and success is False and
                message == ErrorMessage.UNAUTHORIZED_ERROR_MESSAGE)
