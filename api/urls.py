from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from . import views

urlpatterns = [
]


router = SimpleRouter()
router.register(r'orders', views.OrderViewSet)
urlpatterns += router.urls
