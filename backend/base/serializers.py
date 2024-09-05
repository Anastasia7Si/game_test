from rest_framework import serializers

from base.models import PlayerLevel


class PlayerLevelSerializer(serializers.ModelSerializer):
    """Сериализатор уровня игрока."""

    class Meta:
        model = PlayerLevel
        fields = ('id', 'player', 'level',
                  'completed', 'is_completed', 'score')


class LoaderPrizeSerializer(serializers.ModelSerializer):
    """Сериализатор загрузки данных в CSV-файл."""

    prize = serializers.StringRelatedField(
        source='level__levelprize__prize__title'
        )

    class Meta:
        model = PlayerLevel
        fields = ('player', 'level', 'is_completed', 'prize')
