from plugin import CommandPlugin, PluginException
from utils import timestamp_to_date, get_avatar_link, get_player_uuid
import json
import requests
import logging

log = logging.getLogger(__name__)


class MCNameHistory(CommandPlugin):
    """
    Gets the username history for a Minecraft user
    """

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['mchistory', 'mchis']
        self.short_help = 'Prints out username history of a Minecraft username'
        self.help = self.short_help
        self.help_example = ['!mchistory Apple', '!mchis Martin']

    def on_command(self, event, response):
        args = event['text']
        if args:
            message = MCNameHistory.get_name_history(args)
            response.update(attachments=json.dumps([message]))
            self.bot.sc.api_call('chat.postMessage', **response)
        else:
            raise PluginException('No username to lookup! E.g. `!mchistory <username>`')

    @staticmethod
    def get_name_history(username):

        uuid = get_player_uuid(username)
        if not uuid:
            raise PluginException('Failed to lookup UUID for username `%s`' % username)

        name_history_link = 'https://api.mojang.com/user/profiles/%s/names' % uuid
        r = requests.get(name_history_link)
        if r.status_code != requests.codes.ok:
            log.warning("Can't get lookup Minecraft name history for uuid %s!" % uuid)
            raise PluginException('Failed to get username history for UUID `%s`' % uuid)

        return MCNameHistory.build_slack_attachment(username, uuid, name_history_link, r.json())

    @staticmethod
    def build_slack_attachment(username, uuid, link, data):

        attach = {
            'author_name': '%s (Username History) (%s)' % (username, uuid),
            'author_link': link,
            'author_icon': get_avatar_link(username),
            'mrkdwn_in': ['text'],
            'text': ''
        }

        # Go backward in time
        for change in data[::-1]:
            attach['text'] += '`%s` - ' % change['name']
            if 'changedToAt' not in change:
                attach['text'] += '_(original)_'
            else:
                attach['text'] += timestamp_to_date(long(change['changedToAt']))
            attach['text'] += '\n'

        return attach
