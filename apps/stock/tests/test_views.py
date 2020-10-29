import pytest
from django.urls import reverse

from apps.model.stocks import Stocks

"""
https://pytest-django.readthedocs.io/
https://djangostars.com/blog/django-pytest-testing/
"""


@pytest.mark.skip
@pytest.mark.django_db
def test_stock():
    try:
        stock = Stocks.objects.get(stock_code = '060310')
    except Stocks.DoesNotExist:
        raise Exception('DoesNotExist')
    except Stocks.MultipleObjectsReturned:
        raise Exception('MultipleObjectsReturned')

    assert stock.stock_name == '3S'


def test_client(client):
    url = reverse('zzz')
    response = client.get(url)
    assert response.status_code == 200


def test_super_user(admin_client):
    url = reverse('zzz')
    response = admin_client.get(url)
    assert response.status_code == 200
