from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer  # Локальные сериализаторы
from products.models import Watch


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        # Получаем или создаем корзину для пользователя
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(detail=False, methods=['get'], url_path='my-cart')
    def get_my_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        cart = self.get_object()
        watch_id = request.data.get('watch_id')
        quantity = int(request.data.get('quantity', 1))

        watch = Watch.objects.get(id=watch_id)
        # В методе add_item
        if not watch.in_stock:
            return Response(
                {'error': 'Товар отсутствует на складе'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            watch=watch,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='update-item')
    def update_item(self, request):
        cart = self.get_object()
        watch_id = request.data.get('watch_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            watch = Watch.objects.get(id=watch_id)
        except Watch.DoesNotExist:
            return Response(
                {'error': 'Watch not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            item = CartItem.objects.get(cart=cart, watch=watch)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        item.quantity = quantity
        item.save()
        return Response(CartItemSerializer(item).data)


    @action(detail=False, methods=['post'], url_path='remove-item')
    def remove_item(self, request):
        cart = self.get_object()
        watch_id = request.data.get('watch_id')

        try:
            watch = Watch.objects.get(id=watch_id)
        except Watch.DoesNotExist:
            return Response(
                {'error': 'Watch not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            item = CartItem.objects.get(cart=cart, watch=watch)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(status=status.HTTP_200_OK)
