from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, FavoriteAdvertisement


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = FavoriteAdvertisement
        fields = ('user', 'advertisement',)


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft',]

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        qs = Advertisement.objects.filter(creator=self.context['request'].user,status=AdvertisementStatusChoices.OPEN)
        if len(qs)<=10:
            return data
        else:
            raise serializers.ValidationError(f'открытых реклам больше 10, закройте{len(qs)-10} чтоб добавить новые')
