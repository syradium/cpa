import pytest
import orders
import json
from django.core.urlresolvers import reverse


@pytest.fixture
def sample_order_dict(order_dict_factory):
    return order_dict_factory()


@pytest.fixture
def sample_postback_request():
    return {
        'order_id': 10,
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


def test_orderviewset_postback_post_updates_order_if_it_exists(admin_client, order, sample_order_dict):
    sample_order_dict['order_id'], sample_order_dict['pay_status'] = order.order_id, 5
    response = admin_client.post(reverse('api:order-postback'), content_type='application/json', data=json.dumps(sample_order_dict))
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.data['pay_status'] == 5


def test_orderviewset_postback_post_updates_order_if_it_exists_partial(drf_client, order):
    request = {'order_id': order.order_id, 'pay_status': 5}
    response = drf_client.post(reverse('api:order-postback'), data=request)
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.data['pay_status'] == '5'


@pytest.mark.django_db
def test_orderviewset_postback_post_creates_order_set_data_field(client, sample_order_dict):
    response = client.post(reverse('api:order-postback'), data=sample_order_dict)
    assert response.status_code == 200
    order = orders.models.Order.objects.get()
    assert order.data.keys() == sample_order_dict.keys()


def test_orderviewset_delete_removes_order(admin_client, order):
    response = admin_client.delete(reverse('api:order-detail', kwargs={'pk': order.pk}))
    assert response.status_code == 204
    assert orders.models.Order.objects.all().count() == 0


def test_orderviewset_postback_post_correctly_maps_utm(admin_client, order, sample_order_dict):
    sample_order_dict['utm1'], sample_order_dict['order_id'] = 'some_utm_value', order.order_id
    response = admin_client.post(reverse('api:order-postback'), content_type='application/json', data=json.dumps(sample_order_dict))
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.utm_source == 'some_utm_value'
