import allure
import requests

from config import ORDER_URL


class OrderApi:

    @staticmethod
    @allure.step('Создание заказа')
    def create_order(token, ingredients):
        response = requests.post(ORDER_URL, headers=token, json=ingredients)
        return response

    @staticmethod
    @allure.step('Получение заказов пользователя')
    def get_user_orders(token):
        response = requests.get(ORDER_URL, headers=token)
        return response
