import re

import pytest
import requests

from tests.date import get_date_x_days_earlier_than_today


class TestService:
    @pytest.mark.parametrize('name,make_date,response_code', [
        ('тест', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('короб', get_date_x_days_earlier_than_today(days_ago=150), 200),
        ('короб', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('Крассная коробка', get_date_x_days_earlier_than_today(days_ago=150), 200),
        ('фчсмчсмчсм впуцп вап вапкуцйцу', get_date_x_days_earlier_than_today(days_ago=150), 200),
        ('фчсмчсмчсм впуцп вап вапкуцйцур', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('коробка 2', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('box box', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('коробка @', get_date_x_days_earlier_than_today(days_ago=150), 400),
        ('Синяя коробка', get_date_x_days_earlier_than_today(days_ago=365), 400),
        ('Синяя коробка', get_date_x_days_earlier_than_today(days_ago=364), 200),
        ('Зеленая коробка', get_date_x_days_earlier_than_today(days_ago=150), 200),
        ('Желтая коробка', get_date_x_days_earlier_than_today(days_ago=1), 200),
        ('Синяя коробка', get_date_x_days_earlier_than_today(days_ago=0), 400),
    ])
    def test_create(self, name, make_date, response_code, host):
        response = requests.post(url=host+'/api/box', json={'name': name, 'make_date': make_date})
        assert response.status_code == response_code
        if response_code == 200:
            assert re.match('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', response.json())

    @pytest.mark.parametrize('guid,response_code', [
        ('2f11868c-a367-48dc-b4d1-c6706f5258f4', 200),
        ('2f11868c-a367-4444-b4d1-c6706f5258f4', 404),
        ('2f11868c-a3vv67-48dc-b4d1-c6706f5258f4', 400)
    ])
    def test_get(self, guid, response_code, host):
        response = requests.get(url=host+f'/api/box/{guid}')
        assert response.status_code == response_code
        if response_code == 200:
            assert type(response.json()['guid']) == str
            assert re.match('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', response.json()['guid'])
            assert type(response.json()['name']) == str
            assert type(response.json()['age_days']) == int

    @pytest.mark.parametrize('guid,response_code', [
        ('2f11868c-a367-48dc-b4d1-c6706f5258f4', 200),
        ('2f11868c-a367-4444-b4d1-c6706f5258f4', 404),
        ('2f11868c-a3vv67-48dc-b4d1-c6706f5258f4', 400)
    ])
    def test_delete(self, guid, response_code, host):
        response = requests.delete(url=host+f'/api/box/{guid}')
        assert response.status_code == response_code
