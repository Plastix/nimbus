#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import get_player_profile
from plugin import CommandPlugin, PluginException
import logging
import base64

log = logging.getLogger(__name__)


class MCSkin(CommandPlugin):
    """Gets the skin for a Minecraft player"""

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['mcskin', 'skin']
        self.short_help = 'Gets the skin for a Minecraft player'
        self.help = self.short_help
        self.help_example = ['!mcskin Plastix', '!skin Apple']

    def on_command(self, event, response):
        args = event['text']
        if args:
            parts = event['text'].split(' ')
            response.update(attachments=json.dumps([MCSkin.get_skin(parts[0])]))
            self.bot.sc.api_call('chat.postMessage', **response)
        else:
            raise PluginException('No username to fetch skin for! E.g. `!mcskin <username>`')

    @staticmethod
    def get_skin(username):
        response = get_player_profile(username)

        if not response:
            raise PluginException('Failed to fetch player profile for username `%s`' % username)

        # Get player skin string out of profile response
        skin_base64 = response['properties'][0]['value']

        # Decode base64 skin string into response
        skin_decoded = base64.b64decode(skin_base64)
        # Convert response to json
        skin_json = json.loads(skin_decoded)

        return MCSkin.build_slack_attachment(username, skin_json)

    @staticmethod
    def build_slack_attachment(name, response):
        message = {
            'title': '%s (Minecraft Player Skin)' % name,
            'mrkdwn_in': ['text'],
            'text': '',
            'color': 'good'
        }

        textures = response['textures']
        if 'SKIN' in textures:
            message['image_url'] = response['textures']['SKIN']['url']
        else:
            message['text'] = '_Custom skin not set!_'

        return message
