import pytest
import orders
from django.core.urlresolvers import reverse


@pytest.fixture
def sample_order_dict(order_dict_factory):
    return order_dict_factory()


@pytest.fixture
def sample_postback_request():
    return {
        'id': 10,
        'created_on': '2006-10-25 14:30:59',
        'domain': 'domain.com',
        'price': 25,
        'pay_status': 1,
        'pay_sum': 100,
        'utm1': '',
        'utm2': '',
        'utm3': '',
        'utm4': '',
        'status': 'processing',
        'name': 'alex',
        'phone': '+7432552255532',
        'comment': 'foo',
    }

@pytest.mark.django_db
def test_orderviewset_post_creates_an_order(admin_client, sample_order_dict):
    response = admin_client.post(reverse('api:order-list'), data=sample_order_dict)
    assert response.status_code == 201
    assert orders.models.Order.objects.all().count() == 1


@pytest.mark.django_db
def test_orderviewset_postback_post_is_allowed_for_guest(client, sample_order_dict):
    response = client.post(reverse('api:order-postback'), data=sample_order_dict)
    assert response.status_code != 403


@pytest.mark.django_db
def test_orderviewset_postback_post_creates_order_set_data_field(client, sample_order_dict):
    response = client.post(reverse('api:order-postback'), data=sample_order_dict)
    assert response.status_code == 201
    order = orders.models.Order.objects.get()
    assert order.data.keys() == sample_order_dict.keys()


def test_orderviewset_delete_removes_order(admin_client, order):
    response = admin_client.delete(reverse('api:order-detail', kwargs={'pk': order.pk}))
    assert response.status_code == 204
    assert orders.models.Order.objects.all().count() == 0
