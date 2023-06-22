import subprocess
import logging

logger = logging.getLogger(__name__)


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
    if result == "No players found":
        return False
    return True


# List all the players
def list_players():
    if not is_player_running():
        return None
    return _run('playerctl -l').split('\n')


# Get the status of the player
def get_player_status(player):
    return _run(f'playerctl -p {player} status')


# Get the current song
def get_current_song(player):
    return _run(f'playerctl -p {player} metadata --format "{{artist}} - {{title}}"')


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
