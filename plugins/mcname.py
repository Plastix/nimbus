#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import valid_minecraft_username, get_player_uuid_response
from plugin import CommandPlugin
import logging

log = logging.getLogger(__name__)


class MCName(CommandPlugin):
    """Checks if a Minecraft username is registered"""

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['mcname']
        self.short_help = 'Checks whether a Minecraft username is available'
        self.help = self.short_help
        self.help_example = ['!mcname Plastix', '!mcname Apple']

    def on_command(self, bot, event, response):
        args = event['text']
        if args:
            parts = event['text'].split(' ')
            response.update(attachments=json.dumps([MCName.lookup_username(parts[0])]))
            bot.sc.api_call('chat.postMessage', **response)

    @staticmethod
    def lookup_username(name):

        if not valid_minecraft_username(name):
            return MCName.build_slack_attachment(name, None, valid_name=False)

        response = get_player_uuid_response(name)
        return MCName.build_slack_attachment(name, response)

    @staticmethod
    def build_slack_attachment(name, response, valid_name=True):

        message = {
            'title': 'Minecraft Username Lookup',
            'mrkdwn_in': ['text']
        }

        if not valid_name:
            message['text'] = ':warning: Username `%s` is not a valid username!' % name
        elif not response:
            message['text'] = ':white_check_mark: Username `%s` is available!' % name
        elif 'legacy' in response[0]:
            message['text'] = ':x: Username `%s` is taken but not premium!' % name
        else:
            message['text'] = ':x: Username `%s` is taken!' % name

        return message
