import subprocess
import logging

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, name, status, song, album):
        self.name = name
        self.status = status
        self.song = song
        self.album = album
    
    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'{self.name}'


# Run the command and return the output
def _run(command):
    try:
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        logger.debug(f'Command: {command} | Result: {result}')
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f'Command: {e.cmd} | Return code: {e.returncode} | Output: {e.output}')
        return None


# Check if any player is running
def is_player_running():
    result = _run('playerctl -l')
    if result in ['No players found', '']:
        return False
    return True


# Get all the player's list
def get_players_list():
    if not is_player_running():
        return None
    result = _run('playerctl -l').split('\n')
    players = []
    for r in result:
        players.append(get_player_info(r))
    return players


# Get the player info
def get_player_info(player):
    status = get_player_status(player)
    if status in ['No players found', '']:
        return Player(player, None, None, None)
    return Player(player, status, get_current_song(player), get_current_album(player))


# Get the status of the player
def get_player_status(player):
    return _run(f'playerctl -p {player} status')


# Get the current song
def get_current_song(player):
    return _run('playerctl -p '+player+' metadata --format "{{artist}} - {{title}}"')


# Get the current album
def get_current_album(player):
    return _run(f'playerctl -p {player} metadata album')


# Play or pause the current song
def play_pause(player):
    return _run(f'playerctl -p {player} play-pause')


# Skip to the next song
def next_song(player):
    return _run(f'playerctl -p {player} next')


# Skip to the previous song
def previous_song(player):
    return _run(f'playerctl -p {player} previous')
