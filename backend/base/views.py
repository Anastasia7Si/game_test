from datetime import datetime
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Level, LevelPrize, Player, PlayerLevel, Prize
from .serializers import LoaderPrizeSerializer, PlayerLevelSerializer
from .utils import loading_to_csv


class CsvLoaderViewSet(ReadOnlyModelViewSet):
    """Вьюсет выгрузки данных в CSV-файл."""

    queryset = PlayerLevel.objects.all()
    serializer_class = LoaderPrizeSerializer

    @action(detail=False)
    def loading_from_db(self, request):
        """Функция выгрузки данных в CSV-файл."""

        if request.method == 'GET':
            return loading_to_csv(request)


class PlayerLevelViewSet(ModelViewSet):
    """Вьюсет уровня игрока."""

    queryset = PlayerLevel.objects.all()
    serializer_class = PlayerLevelSerializer

    @action(detail=False)
    def award_prize(request, player_id, level_id, prize_id):
        """Функция присвоения игроку приза за прохождение уровня."""

        if request.method == 'POST':
            player = Player.objects.get(player_id=player_id)
            level = Level.objects.get(id=level_id)
            prize = Prize.objects.get(id=prize_id)
            player_level = PlayerLevel.objects.filter(
                player=player, level=level
                ).first()
            if player_level.is_completed:
                level_prize, created = LevelPrize.objects.get_or_create(
                    level=level, prize=prize
                    )
                if created:
                    level_prize.received = datetime.now()
                    level_prize.save()
                    return (f'Приз {prize.title} выдан игроку '
                            f'{player.player_id} за завершение '
                            f'{level.title} уровня')
                else:
                    return (f'Игрок {player.player_id} уже получил '
                            f'{prize.title} приз за уровень {level.title}.')
            else:
                return (f'Игрок {player.player_id} не завершил уровень '
                        f'{level.title} и не может получить приз '
                        f'{prize.title}.')
