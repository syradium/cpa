from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/list.html'
