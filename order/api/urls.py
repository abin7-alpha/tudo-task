from django.urls import path
from order.api.views.order_view import order_view

urlpatterns = [
    path('order-item', order_view, name='order_item'),
]