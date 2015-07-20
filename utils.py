from datetime import date
import re


def valid_minecraft_username(name):
    """
    Returns whether the specified string is a valid Minecraft username
    """
    return re.match(r'^[a-zA-Z0-9_]{1,16}$', name)


def timestamp_to_date(timestamp):
    """
    Converts Java timestamp to Python date
    1241711346274 -> 2009-05-07

    """
    return str(date.fromtimestamp(timestamp / 1000.0))


def get_avatar_link(player_name):
    """
    Gets the 16x16 Avatar for a Minecraft username
    (Thank you OCN avatar server!)
    """
    return 'https://avatar.oc.tc/%s/16@2x.png' % str(player_name)


def get_player_link(player_name):
    """
    Gets the OCN profile link for a Minecraft username
    """
    return 'http://oc.tc/%s' % str(player_name)
