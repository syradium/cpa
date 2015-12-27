from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('orders:list'), permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout_then_login, name='logout'),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
]
