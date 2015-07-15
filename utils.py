import re


def valid_minecraft_username(name):
    """
    Returns whether the specified string is a valid Minecraft username
    """
    return re.match(r'^[a-zA-Z0-9_]{1,16}$', name)
