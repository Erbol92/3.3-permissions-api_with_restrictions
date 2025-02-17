from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='creator', lookup_expr='icontains')  # Поиск по заголовку

    class Meta:
        model = Advertisement
        fields = ['creator', 'status']  # Укажите поля, по которым можно фильтровать
