import logging
import playerctl
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)


def main_page_items():
    items = []
    players = playerctl.get_players_list()
    logger.debug(f'Players: {players}')
    
    if players is None:
        items.append(ExtensionResultItem(icon='images/record-vinyl.png',
                                         name='No players found',
                                         description='Please open a player',
                                         on_enter=HideWindowAction()))
    else:
        for player in players:
            items.append(ExtensionResultItem(icon='images/music.png',
                                             name=player.name.split('.')[0],
                                             description=f'{player.status}: {player.song}',
                                             on_enter=ExtensionCustomAction({'name': player.name,
                                                                             'action': 'player_page'},
                                                                            keep_app_open=True)))
    return items


def player_page_items(player):
    items = []
    player = playerctl.get_player_info(player)
    logger.debug(f'Player: {player}')
    
    if player.status == 'Playing':
        items.append(ExtensionResultItem(icon='images/pause.png',
                                        name='Pause',
                                        on_enter=ExtensionCustomAction({'name': player,
                                                                        'action': 'play-pause'})))
    else:
        items.append(ExtensionResultItem(icon='images/play.png',
                                        name='Play',
                                        on_enter=ExtensionCustomAction({'name': player,
                                                                        'action': 'play-pause'})))
    items.append(ExtensionResultItem(icon='images/step-forward.png',
                                     name='Next',
                                     on_enter=ExtensionCustomAction({'name': player,
                                                                     'action': 'next'})))
    items.append(ExtensionResultItem(icon='images/step-backward.png',
                                     name='Previous',
                                     on_enter=ExtensionCustomAction({'name': player,
                                                                     'action': 'previous'})))
    now_status = f'Now {player.status}'
    if player.album:
        now_status = f'{now_status}: {player.album}'
    items.append(ExtensionResultItem(icon='images/music.png',
                                        name=player.song,
                                        description=now_status,
                                        on_enter=HideWindowAction()))
    return items
