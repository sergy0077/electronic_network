from .models import NetworkObject, Product, Factory, RetailNetwork, Entrepreneur, Supplier
from .serializers import NetworkObjectSerializer, ProductSerializer, FactorySerializer, RetailNetworkSerializer, EntrepreneurSerializer, SupplierSerializer
from .permissions import IsActiveEmployee, IsOwnerOrReadOnly, get_user_token
import django_filters
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list
from django.http import JsonResponse


def factory_list_view(request):
    """
    Получение токена пользователя (используем get_user_token)
    """
    user_token = get_user_token(request)

    # Задаем URL и заголовки
    url = 'http://example.com/api/factories/'
    headers = {'Authorization': f'Bearer {user_token}'}

    # Отправляем GET запрос
    response = requests.get(url, headers=headers)

    # Обрабатываем ответ и возвращаем результат
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Something went wrong'}, status=response.status_code)


class NetworkObjectFilter(django_filters.FilterSet):
    """
    Фильтрацию объектов NetworkObject по стране
    """
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = NetworkObject
        fields = ['country', 'city']


class NetworkObjectViewSet(viewsets.ModelViewSet):
    """
    Представление для NetworkObject
    """
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_class = NetworkObjectFilter

    @action(detail=False, methods=['get'])
    def filter_network_objects(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Представление для Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class FactoryViewSet(viewsets.ModelViewSet):
    """
    Представление для Factory
    """
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, methods=['post'])
    def clear_debt(self, request, pk=None):
        factory = self.get_object()
        # Проверяем, есть ли параметр 'amount' в теле запроса
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required in the request body'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Пробуем преобразовать значение amount в Decimal
            validate_comma_separated_integer_list(amount)
        except ValidationError:
            return Response({'error': 'Invalid amount format'}, status=status.HTTP_400_BAD_REQUEST)
        # Уменьшаем задолженность на указанную сумму
        factory.debt_to_supplier -= int(amount)
        # Если задолженность становится отрицательной, устанавливаем её в 0
        if factory.debt_to_supplier < 0:
            factory.debt_to_supplier = 0
        factory.save()
        return Response({'message': f'Debt reduced by {amount}. New debt: {factory.debt_to_supplier}'},
                        status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()

    actions = ['clear_debt']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    http_method_names = ['get', 'post', 'head', 'options', 'put', 'patch', 'delete']


class RetailNetworkViewSet(viewsets.ModelViewSet):
    """
    Представление для RetailNetwork
    """
    queryset = RetailNetwork.objects.all()
    serializer_class = RetailNetworkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        entrepreneurs = Entrepreneur.objects.all()
        serializer = EntrepreneurSerializer(entrepreneurs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EntrepreneurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        serializer = EntrepreneurSerializer(entrepreneur)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        serializer = EntrepreneurSerializer(entrepreneur, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        entrepreneur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EntrepreneurViewSet(viewsets.ModelViewSet):
    """
    Представление для Entrepreneur
    """
    queryset = Entrepreneur.objects.all()
    serializer_class = EntrepreneurSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        entrepreneurs = Entrepreneur.objects.all()
        serializer = EntrepreneurSerializer(entrepreneurs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EntrepreneurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        serializer = EntrepreneurSerializer(entrepreneur)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        serializer = EntrepreneurSerializer(entrepreneur, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        entrepreneur = self.get_object()
        entrepreneur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Представление для Supplier
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = SupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        supplier = self.get_object()
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        supplier = self.get_object()
        serializer = SupplierSerializer(supplier, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        supplier = self.get_object()
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@authentication_classes([])
def api_index(request):
    """
    Представление для главной страницы
    """
    return JsonResponse({'message': 'Welcome to the API index!'})
