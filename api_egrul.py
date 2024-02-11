"""Модуль возвращает данные юридического лица по ИНН"""

import requests
from pprint import pprint

from . import exceptions
from .const import END_POINT_URL, END_POINT_2_URL, CORRESP_DB_AND_RESP
# from models import LegEnt


def get_token(inn: str) -> str:
    """Получает словарь с токеном для второго запроса."""
    params: dict = {'query': inn}
    try:
        response = requests.post(
            END_POINT_URL,
            json=params,
        )

    except requests.RequestException as request_error:
        raise exceptions.ApiError(request_error)
    try:
        token_response: dict = response.json()
    except (requests.exceptions.InvalidJSONError, TypeError):
        raise exceptions.ApiError('Invalid JSON Error')
    if token_response['captchaRequired'] is not False:
        raise exceptions.ApiError('сервер запрашивает проверку captcha')
    return token_response['t']


def get_data_from_api(token: str) -> dict:
    """Получает словарь с данными организации по токену."""

    full_url = END_POINT_2_URL+token
    response = requests.get(
        full_url
    )
    try:
        data_response = response.json()
    except (requests.exceptions.InvalidJSONError, TypeError):
        raise exceptions.ApiError('Invalid JSON Error')
    governor: list = data_response['rows'][0]['g'].split(': ')
    date_of_creation: list = data_response['rows'][0]['r'].split('.')
    work_dict: dict = data_response['rows'][0]
    work_dict['g1'] = governor[0]
    work_dict['g2'] = governor[1]
    work_dict['r'] = (
        f'{date_of_creation[2]}-{date_of_creation[1]}-{date_of_creation[0]}'
    )
    result_dict: dict = {}
    for db_key, resp_key in CORRESP_DB_AND_RESP.items():
        result_dict[db_key] = work_dict[resp_key]
    return result_dict


def get_data_from_api_with_inn(inn: str) -> dict:
    """Получает словарь с данными организации по ИНН."""
    token: str = get_token(inn)
    data: dict = get_data_from_api(token)
    return data


if __name__ == '__main__':
    inn: str = input('Введите ИНН организации: ')
    token: str = get_token(inn)
    data = get_data_from_api(token)
    pprint(data)
    # choice = input('Записать данные в базу? (y = да) ')
    # if choice == 'y':
    #     LegEnt.objects.create(**data)
