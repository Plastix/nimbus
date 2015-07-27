from bs4 import BeautifulSoup
from plugin import CommandPlugin, PluginException
import requests
import json


class PlayingMaps(CommandPlugin):
    """
    Parses Overcast's maps page and prints currently playing maps
    """

    ocn_maps_link = 'https://oc.tc/maps'

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['playingmaps']
        self.short_help = 'Prints out currently playing maps on the Overcast Network'
        self.help = self.short_help
        self.help_example = ['!playingmaps']

    @staticmethod
    def build_slack_attachment(data):

        attach = {
            'title': 'Overcast Network - Currently playing maps',
            'text': '',
            'mrkdwn_in': ['text'],
            'title_link': PlayingMaps.ocn_maps_link
        }

        for server in sorted(data.keys()):
            attach['text'] += '*%s:* ' % server
            attach['text'] += ', '.join(data[server])
            attach['text'] += '\n'

        return attach

    @staticmethod
    def parse_maps_list():
        r = requests.get(PlayingMaps.ocn_maps_link)

        if r.status_code != requests.codes.ok:
            raise PluginException('Failed to fetch currently playing Overcast Network maps!')

        soup = BeautifulSoup(r.text)

        # Key: Server Name
        # Value: List of currently playing maps
        data = {}
        maps_elements = soup.find_all('div', class_='map thumbnail')
        for map in maps_elements:
            map_name = map.find('h1', class_='lead').a.contents[0]

            # Wrapper around server labels
            servers_div = map.find('div', class_='servers')
            # Labels of playing servers
            playing_on = servers_div.find_all('a', class_='label label-warning')
            for server in playing_on:
                server_name = server.contents[0]
                # Check if server is not in dictionary
                if not data.get(server_name):
                    data[server_name] = []
                data[server_name].append(map_name)

        # Return slack attachment with parsed data
        return PlayingMaps.build_slack_attachment(data)

    def on_command(self, bot, event, response):
        response.update(attachments=json.dumps([PlayingMaps.parse_maps_list()]))
        bot.sc.api_call('chat.postMessage', **response)
