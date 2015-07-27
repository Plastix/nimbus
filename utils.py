from datetime import date
import json
import re
import requests
import logging

log = logging.getLogger(__name__)


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


def get_urls(text):
    """
    Gets the URLS in a Slack message text.
    Returns a list of URL Strings
    """
    urls = list()
    # Find all sequences matching <foo|bar>
    for sequence in re.findall(r'<(.*?)>', text):
        # Only look for Slack URL formats, not channels, users, or special commands
        if not sequence.startswith(('#C', '@U', '!')):
            url = sequence
            if '|' in sequence:
                parts = sequence.split('|')
                if len(parts) > 1:
                    # If there is a label, URL is before label
                    url = parts[0]

            urls.append(url)

    return urls


def strip_url_formatting(text):
    """
    Slack does URL parsing to include labels in URLs. This methods accepts the parsed input and strips the URL formatting
    to return the raw input.

    An example slack message '<http://www.google.com|www.google.com>' becomes 'www.google.com'
    If there is no label: '<http://oc.tc>' becomes 'http://oc.tc'
    Works with multiple urls per message!
    """

    # Find all sequences matching <foo|bar>
    for sequence in re.findall(r'<(.*?)>', text):
        # Only look for Slack URL formats, not channels, users, or special commands
        if not sequence.startswith(('#C', '@U', '!')):
            to_replace = '<%s>' % sequence
            if '|' in sequence:
                parts = sequence.split('|')
                if len(parts) > 1:
                    # Replace the text sequence with label of URL only
                    text = text.replace(to_replace, parts[1])
            else:
                # If no | replace with sequence to strip < >
                text = text.replace(to_replace, sequence)

    return text


def get_player_uuid_response(username):
    """
    Get's the json response for Mojangs's uuid API for a given username
    Returns response if found, else None
    """
    # Don't even bother checking API for invalid names
    if not valid_minecraft_username(username):
        return

    profile_link = 'https://api.mojang.com/profiles/minecraft'
    payload = json.dumps(username)

    header = {'Content-type': 'application/json'}
    r = requests.post(profile_link, headers=header, data=payload)

    if r.status_code != requests.codes.ok:
        log.warning("Can't get lookup Minecraft profile for name %s!" % username)
        return

    return r.json()


def get_player_uuid(username):
    """
    Lookups the UUID for a Minecraft username using Mojang's profile API
    Returns a string of the UUID if found, or None if player doesn't exist
    """

    response = get_player_uuid_response(username)
    if response:
        return str(response[0]['id'])


def get_player_profile(username):
    """
    Returns the json response for Mojang's profile API for the given username
    Returns resonse, else None
    """
    uuid = get_player_uuid(username)
    if not uuid:
        return

    profile_url = 'https://sessionserver.mojang.com/session/minecraft/profile/%s' % uuid
    r = requests.get(profile_url)

    if r.status_code != requests.codes.ok:
        return

    return r.json()
