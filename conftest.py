from distutils import dir_util
from django_redis import get_redis_connection
from pytest_factoryboy import register
from unittest.mock import patch
import json
import os
import pytest
import redis_lock
import tests.factories


@pytest.fixture
def drf_client(db, admin_user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture(autouse=True)
def clear_redis():
    conn = get_redis_connection("default")
    redis_lock.reset_all(conn)
    conn.flushdb()


@pytest.fixture
def datadir(tmpdir, request):
    filename = request.module.__file__
    test_dir = os.path.join(os.path.dirname(filename), 'assets')

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


register(tests.factories.OrderDictFactory)
register(tests.factories.OrderFactory)
