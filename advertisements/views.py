from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rest_framework import serializers
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='creator', lookup_expr='icontains')  # Поиск по заголовку

    class Meta:
        model = Advertisement
        fields = ['creator']  # Укажите поля, по которым можно фильтровать


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [AnonRateThrottle]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    @action(detail=True, methods=['post'], url_path='favorite')
    def add_to_favorites(self, request, pk=None):
        advertisement = self.get_object()
        user = request.user
        print(user)
        # Проверка, является ли пользователь создателем объявления
        if advertisement.creator == user:
            raise serializers.ValidationError('Вы не можете добавить свое объявление в избранное')
        else:
            # Добавление в избранное
            favorite, created = FavoriteAdvertisement.objects.get_or_create(user=user, advertisement=advertisement)

            if created:
                return Response({"detail": "Объявление добавлено в избранное."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Объявление уже в избранном."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='favorites')
    def list_favorites(self, request):
        user = request.user
        favorites = FavoriteAdvertisement.objects.filter(user__id=user.id).select_related('advertisement')
        serializer = AdvertisementSerializer([fav.advertisement for fav in favorites], many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["destroy", "update", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []
