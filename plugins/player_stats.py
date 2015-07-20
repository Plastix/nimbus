#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from utils import valid_minecraft_username, get_player_link, get_avatar_link
from plugin import CommandPlugin


class PlayerStats(CommandPlugin):
    """
    Scrapes Overcast Network player stats
    """

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['player', 'stats']
        self.short_help = 'Lookup Overcast Network player stats'
        self.help = self.short_help
        self.help_example = ['!player Plastix', '!player bcbwilla']

    def on_command(self, bot, event, response):
        args = event['text']
        if args:
            message = PlayerStats.scrape_stats(args)
            response.update(attachments=json.dumps([message]))
            bot.sc.api_call('chat.postMessage', **response)

    @staticmethod
    def scrape_stats(player_name):
        """
        Scrapes Overcast Network Player Stats
        Based on code by @McSpider
        https://github.com/McSpider/Overcast-IRC-Bot/blob/master/_functions/player.py
        """
        result = {
            'name': player_name,
            'error': ''
        }

        if not valid_minecraft_username(player_name):
            result['error'] = ':warning: Invalid player name!'
            return PlayerStats.build_slack_attachment(result)

        r = requests.get(get_player_link(player_name))

        if r.status_code != requests.codes.ok:
            if r.status_code == 404:
                result['error'] = '404 - User not found'
            if r.status_code == 522:
                result['error'] = '522 - Request Timed Out'
            else:
                result['error'] = 'Request Exception - Code: ' + str(r.status_code)
        else:
            soup = BeautifulSoup(r.text)
            if soup.find("h4", text=["Account Suspended"]):
                result['error'] = 'User Account Suspended'
            elif soup.find("p", text=["Page Exploded"]):
                result['error'] = '404 - User not found'
            elif soup.find("small", text=["server joins"]):
                result['kills'] = soup.find("small", text=["kills"]).findParent('h2').contents[0].strip('\n')
                result['deaths'] = soup.find("small", text=["deaths"]).findParent('h2').contents[0].strip('\n')
                result['friends'] = soup.find("small", text=["friends"]).findParent('h2').contents[0].strip('\n')
                result['kd_ratio'] = soup.find("small", text=["kd ratio"]).findParent('h2').contents[0].strip('\n')
                result['kk_ratio'] = soup.find("small", text=["kk ratio"]).findParent('h2').contents[0].strip('\n')
                result['joins'] = soup.find("small", text=["server joins"]).findParent('h2').contents[0].strip('\n')
                result['raindrops'] = soup.find("small", text=["raindrops"]).findParent('h2').contents[0].strip('\n')

                result['wools'] = "0"
                result['cores'] = "0"
                result['monuments'] = "0"

                wools_element = soup.find("small", text=["wools placed"])
                if wools_element:
                    result['wools'] = wools_element.findParent('h2').contents[0].strip('\n')

                cores_element = soup.find("small", text=["cores leaked"])
                if cores_element:
                    result['cores'] = cores_element.findParent('h2').contents[0].strip('\n')

                monuments_element = soup.find("small", text=["monuments destroyed"])
                if monuments_element:
                    result['monuments'] = monuments_element.findParent('h2').contents[0].strip('\n')
            else:
                result['error'] = 'Invalid user!'

        return PlayerStats.build_slack_attachment(result)

    @staticmethod
    def build_slack_attachment(stats):
        """
        Builds the JSON attachment for the Slack message
        """
        message = {}
        error = stats['error']
        name = stats['name']
        message['author_name'] = name + ' (Player Stats)'

        if error:
            message['color'] = 'danger'
            message['text'] = error
        else:
            message['color'] = 'good'
            message['author_link'] = get_player_link(name)
            message['author_icon'] = get_avatar_link(name)

            text = 'Kills: `%s` Deaths: `%s` KD: `%s` KK: `%s`\nWools: `%s` Cores: `%s` Monuments: `%s`\nFriends: `%s` Joins: `%s` Raindrops: `%s`' % (
                stats['kills'],
                stats['deaths'], stats['kd_ratio'], stats['kk_ratio'], stats['wools'], stats['cores'],
                stats['monuments'],
                stats['friends'], stats['joins'], stats['raindrops'])
            message['text'] = text
            message['mrkdwn_in'] = ['text']

        return message
