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


def strip_url_formatting(text):
    """
    Slack does URL parsing to include labels in URLs. This methods accepts the parsed input and strips the URL formatting
    to return the raw input.

    An example slack message '<http://www.google.com|www.google.com>' becomes 'www.google.com'
    Works with multiple urls per message!
    """

    # Find all sequences matching <foo|bar>
    for sequence in re.findall(r'<(.*?)>', text):
        # Only look for Slack URL formats, not channels, users, or special commands
        if not sequence.startswith(('#C', '@U', '!')):
            if '|' in sequence:
                parts = sequence.split('|')
                if len(parts) > 1:
                    # Replace the text sequence with label of URL only
                    text = text.replace('<%s>' % sequence, parts[1])
    return text
