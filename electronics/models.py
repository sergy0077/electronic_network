from django.db import models
from django.utils import timezone


class BaseNetworkObject(models.Model):
    """
    Абстрактный класс для наследования
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Supplier(BaseNetworkObject):
    """
    Модель Поставщика
    """
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Supplier)"


class Product(models.Model):
    """
    Модель Товара
    """
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='supplied_products')
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NetworkObject(BaseNetworkObject):
    """
    Модель сети по продаже электроники
    """
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    )

    level = models.PositiveIntegerField(choices=LEVEL_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='sub_network_objects')

    def __str__(self):
        return f"{self.name} (NetworkObject)"


class Factory(BaseNetworkObject):
    """
    Модель Завода
    """
    network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='factories')
    products = models.ManyToManyField(Product, related_name='factories', blank=True)
    previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_factories')
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Factory)"


class RetailNetwork(BaseNetworkObject):
    """
    Модель Розничной сети
    """
    network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='retail_networks')
    products = models.ManyToManyField(Product, related_name='retail_networks', blank=True)
    previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_retail_networks')
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (RetailNetwork)"


class Entrepreneur(BaseNetworkObject):
    """
    Модель Индивидуального предпринимателя
    """
    network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='entrepreneurs')
    products = models.ManyToManyField(Product, related_name='entrepreneurs', blank=True)
    previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_entrepreneurs')
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Entrepreneur)"




# from django.db import models
# from django.utils import timezone
#
#
# class BaseNetworkObject(models.Model):
#     """
#     Абстрактный класс для наследования
#     """
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     country = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     street = models.CharField(max_length=255)
#     house_number = models.CharField(max_length=10)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#
#     class Meta:
#         abstract = True
#
#
# class Supplier(BaseNetworkObject):
#     """
#     Модель Поставщика
#     """
#     debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#
#
# class Product(models.Model):
#     """
#     Модель Товара
#     """
#     name = models.CharField(max_length=255)
#     model = models.CharField(max_length=255)
#     release_date = models.DateField()
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='supplied_products')
#     debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class NetworkObject(BaseNetworkObject):
#     """
#     Модель сети по продаже электроники
#     """
#     LEVEL_CHOICES = (
#         (0, 'Завод'),
#         (1, 'Розничная сеть'),
#         (2, 'Индивидуальный предприниматель'),
#     )
#
#     level = models.PositiveIntegerField(choices=LEVEL_CHOICES)
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='sub_network_objects')
#
#
# class Factory(BaseNetworkObject):
#     """
#     Модель Завода
#     """
#     network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='factories')
#     products = models.ManyToManyField(Product, related_name='factories', blank=True)
#     previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_factories')
#     debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#
#
# class RetailNetwork(BaseNetworkObject):
#     """
#     Модель Розничной сети
#     """
#     network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='retail_networks')
#     products = models.ManyToManyField(Product, related_name='retail_networks', blank=True)
#     previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_retail_networks')
#     debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#
#
# class Entrepreneur(BaseNetworkObject):
#     """
#     Модель Индивидуального предпринимателя
#     """
#     network_object = models.OneToOneField(NetworkObject, on_delete=models.CASCADE, null=True, blank=True)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='entrepreneurs')
#     products = models.ManyToManyField(Product, related_name='entrepreneurs', blank=True)
#     previous_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_entrepreneurs')
#     debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#
