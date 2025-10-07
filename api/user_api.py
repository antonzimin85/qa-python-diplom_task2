import allure
import requests

import config


class UserApi:

    @staticmethod
    @allure.step('Регистрация нового пользователя')
    def register_new_user(user_data):
        response = requests.post(config.REGISTER_USER_URL, json=user_data)
        return response

    @staticmethod
    @allure.step('Логин пользователя')
    def login_user(credentials):
        response = requests.post(config.LOGIN_URL, json=credentials)
        return response

    @staticmethod
    @allure.step('Обновление данных пользователя')
    def update_user_data(token, user_data):
        response = requests.patch(config.USER_URL, headers=token, json=user_data)
        return response

    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(token):
        headers = {'Authorization': token}
        response = requests.delete(config.USER_URL, headers=headers)
        return response
