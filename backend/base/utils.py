import csv
from django.http import HttpResponse
from io import StringIO

from base.models import LevelPrize, PlayerLevel


def loading_to_csv(request):
    """Функция выгрузки данных в csv-файл."""

    players_level = PlayerLevel.objects.all()
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer, dialect='excel')
    # Либо, непосредственная запиь в файл на сервере
    # with open('player_levels_data.csv', 'w') as file:
    # writer = csv.writer(file)
    writer.writerow(['Player_id', 'Level_title', 'Is_completed', 'Prize'])
    for player_level in players_level:
        player_id = player_level.player.player_id
        level_title = player_level.level.title
        is_completed = player_level.is_completed
        prize = LevelPrize.objects.filter(
            level=player_level.level
            ).first().prize.title if LevelPrize.objects.filter(
                level=player_level.level
                ).exists() else None
        writer.writerow([player_id, level_title, is_completed, prize])

    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['charset'] = 'utf-8'
    response['Content-Disposition'] = ('attachment; '
                                       'filename="player_levels_data.csv"')
    return response
