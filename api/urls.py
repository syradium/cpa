from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from . import views

urlpatterns = [
    url(r'^$', None, name='name'),
]


router = SimpleRouter()
router.register(r'orders', views.OrderViewSet)
urlpatterns = router.urls
