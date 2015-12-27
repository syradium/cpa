from django.core.urlresolvers import reverse


def test_orderlistview_uses_correct_template(admin_client):
    response = admin_client.get(reverse('orders:list'))
    assert response.status_code == 200
    assert 'orders/list.html' in response.template_name
