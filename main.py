import logging
import playerctl
from playerctl.items import main_page_items, player_page_items
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

logger = logging.getLogger(__name__)


class PlayerctlExtension(Extension):

    def __init__(self):
        super(PlayerctlExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        keyword = event.get_keyword()
        extension.logger.debug(f'log preference {extension.preferences}')
        
        if keyword == extension.preferences['playerctl_kw']:
            items = main_page_items()
        elif keyword == extension.preferences['playerctl_def_kw']:
            items = player_page_items(extension.preferences['playerctl_def_player'])

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        player = data.get('name')
        action = data.get('action')
        
        if action == 'player_page':
            return RenderResultListAction(player_page_items(player))
        elif action == 'play-pause':
            playerctl.play_pause(player)
        elif action == 'next':
            playerctl.next_song(player)
        elif action == 'previous':
            playerctl.previous_song(player)


if __name__ == '__main__':
    PlayerctlExtension().run()
