#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from plugin import CommandPlugin


class MojangStatus(CommandPlugin):
    """
    Prints the status of Mojang's services
    """
    mojang_status_link = 'http://status.mojang.com/check'

    status = {
        'green': ':white_check_mark:',
        'yellow': ':warning:',
        'red': ':x:',
    }

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['mojang', 'mcstatus']
        self.short_help = 'Prints the status of Mojang\'s services'
        self.help = self.short_help
        self.help_example = ['!mojang']

    @staticmethod
    def build_slack_attachment(data):
        response = {}
        response['title'] = 'Mojang Status Summary'
        response['title_link'] = 'https://help.mojang.com/'
        response['text'] = ''
        response['mrkdwn_in'] = ['text']

        for service in data:
            service_name = next(iter(service.keys()))
            color = service[service_name]
            stat = MojangStatus.status.get(color, ':question:')
            response['text'] += '%s *%s*\n' % (stat, service_name)

        return response

    @staticmethod
    def get_mojang_status():
        r = requests.get(MojangStatus.mojang_status_link)

        if r.status_code != 200:
            print "Can't get Mojang Status!"
            return
        else:
            status = r.json()

            return MojangStatus.build_slack_attachment(status)

    def on_command(self, bot, event, response):
        response.update(attachments=json.dumps([MojangStatus.get_mojang_status()]))
        bot.sc.api_call('chat.postMessage', **response)
