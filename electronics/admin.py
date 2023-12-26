from django.contrib import admin
from .models import NetworkObject, Product, Factory, RetailNetwork, Supplier, Entrepreneur
from django.utils.html import format_html
from django.urls import reverse


class NetworkObjectAdmin(admin.ModelAdmin):
    """
    В админ-страничку Сети по продаже электроники добавлены:
    - метод supplier_link для создания ссылки на объект «Поставщика»;
    - фильтры по названию города и поставщика;
    - метод «clear_debt», очищающий задолженность перед поставщиком у выбранных объектов
    """
    list_display = ('name', 'email', 'country', 'city', 'street', 'house_number', 'supplier_link', 'is_active', 'created_at')
    list_filter = ('city', 'supplier')
    search_fields = ['city']
    actions = ['clear_debt']

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="{}">{}</a>', reverse('admin:electronics_networkobject_change', args=[obj.supplier.id]),
                               obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Supplier'

    def clear_debt(modeladmin, request, queryset):
        queryset.update(debt_to_supplier=0)

    clear_debt.short_description = "Clear selected objects' debt to supplier"


class ProductAdmin(admin.ModelAdmin):
    """
    Админ-страничка Товара
    """
    actions = ['clear_debt']
    list_display = ('name', 'model', 'release_date', 'supplier', 'debt_to_supplier', 'created_at')
    search_fields = ['city']


class FactoryAdmin(admin.ModelAdmin):
    """
    Админ-страничка Завода
    """
    list_display = ('name', 'email', 'country', 'city', 'street', 'house_number', 'created_at', 'products_list', 'network_object_supplier')

    def products_list(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    products_list.short_description = 'Products'

    def network_object_supplier(self, obj):
        # Проверка наличия связанного NetworkObject
        if obj.network_object:
            return obj.network_object.supplier.name
        else:
            return '-'

    network_object_supplier.short_description = 'Supplier (from NetworkObject)'


class EntrepreneurAdmin(admin.ModelAdmin):
    """
    Админ-страничка Индивидуального предпринимателя
    """
    list_display = ('name', 'email', 'country', 'city', 'street', 'house_number', 'created_at', 'products_list', 'supplier')

    def products_list(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    products_list.short_description = 'Products'

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="{}">{}</a>', reverse('admin:electronics_networkobject_change', args=[obj.supplier.id]),
                               obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Supplier'


class RetailNetworkAdmin(admin.ModelAdmin):
    """
    Админ-страничка Розничной сети
    """
    list_display = ('name', 'email', 'country', 'city', 'street', 'house_number', 'created_at', 'products_list', 'network_object_supplier')

    def products_list(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    products_list.short_description = 'Products'

    def network_object_supplier(self, obj):
        # Проверка наличия связанного NetworkObject
        if obj.network_object:
            return obj.network_object.supplier.name
        else:
            return '-'

    network_object_supplier.short_description = 'Supplier (from NetworkObject)'


"""
Добавили все классы к регистрации, чтобы они применились
"""
admin.site.register(NetworkObject, NetworkObjectAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(RetailNetwork, RetailNetworkAdmin)
admin.site.register(Entrepreneur, EntrepreneurAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)