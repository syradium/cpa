from . import serializers
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
import orders


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = orders.models.Order.objects.all()

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def postback(self, request):
        request.data['data'] = request.data.dict()
        return self.create(request)
