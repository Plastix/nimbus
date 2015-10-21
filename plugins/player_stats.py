#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from utils import valid_minecraft_username, get_player_link, get_avatar_link
from plugin import CommandPlugin, PluginException


class PlayerStats(CommandPlugin):
    """
    Scrapes Overcast Network player stats
    """

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['player', 'stats']
        self.short_help = 'Lookup Overcast Network player stats'
        self.help = self.short_help
        self.help_example = ['!player Plastix', '!player bcbwilla']

    def on_command(self, event, response):
        args = event['text']
        if args:
            message = PlayerStats.scrape_stats(args)
            response.update(attachments=json.dumps([message]))
            self.bot.sc.api_call('chat.postMessage', **response)
        else:
            raise PluginException('No player to lookup stats! E.g. `!player <username>`')

    @staticmethod
    def scrape_stats(player_name):
        """
        Scrapes Overcast Network Player Stats
        Based on code by @McSpider
        https://github.com/McSpider/Overcast-IRC-Bot/blob/master/_functions/player.py

        Updated to work with new Overcast Network ranked profiles
        """
        result = {
            'name': player_name,
        }

        if not valid_minecraft_username(player_name):
            raise PluginException(':warning: Invalid player name!')

        r = requests.get(get_player_link(player_name))

        if r.status_code != requests.codes.ok:
            if r.status_code == 404:
                raise PluginException('404 - User not found')
            if r.status_code == 522:
                raise PluginException('522 - Request Timed Out')
            else:
                raise PluginException('Request Exception - Code: %s' % str(r.status_code))
        else:
            soup = BeautifulSoup(r.text)
            if soup.find("h4", text=["Account Suspended"]):
                result['error'] = 'User Account Suspended'
            elif soup.find("p", text=["Page Exploded"]):
                result['error'] = '404 - User not found'
            elif soup.find("div", {'class': 'stats'}):
                # Check if user is unrated
                if soup.find('div', {'class': 'unqualified'}):
                    result['rank'] = 'N/A'
                    result['rating'] = 'N/A'
                # Else get their rank and rating
                else:
                    rank = soup.find('div', text=['rank']).findNext('a').contents
                    result['rank'] = '%s%s' % (rank[0].strip(), rank[1].text.strip())
                    result['rating'] = soup.find('div', text=['rating']).findNext('div').text.strip()

                # Get kills, deaths, and calculate kd ratio
                result['kills'] = soup.find('div', text=['kills']).findNext('div')['title'].split(' ')[0].strip()
                result['deaths'] = soup.find('div', text=['deaths']).findNext('div')['title'].split(' ')[0].strip()
                result['kd_ratio'] = '%.2f' % (float(result['kills']) / max(1, float(result['deaths'])))

                # Get objectives if there are any
                if soup.find('p', text=['No objectives completed']):
                    result['wools'] = 0
                    result['cores'] = 0
                    result['monuments'] = 0
                else:
                    objectives = soup.find('div', {'id': 'objectives'})
                    result['wools'] = objectives.find('small', text=['wools placed']).parent.contents[0].strip()
                    result['monuments'] = objectives.find('small', text=['monuments destroyed']).parent.contents[
                        0].strip()
                    result['cores'] = objectives.find('small', text=['cores leaked']).parent.contents[0].strip()
            else:
                raise PluginException('Invalid user!')

            return PlayerStats.build_slack_attachment(result)

    @staticmethod
    def build_slack_attachment(stats):
        """
        Builds the JSON attachment for the Slack message
        """
        message = {}
        name = stats['name']
        message['author_name'] = '%s (Player Stats)' % name
        message['color'] = 'good'
        message['author_link'] = get_player_link(name)
        message['author_icon'] = get_avatar_link(name)

        text = 'Rank: `%s` Rating: `%s`\nKills: `%s` Deaths: `%s` KD: `%s`\nWools: `%s` Cores: `%s` Monuments: `%s`' % (
            stats['rank'],
            stats['rating'], stats['kills'],
            stats['deaths'], stats['kd_ratio'], stats['wools'], stats['cores'], stats['monuments'])
        message['text'] = text
        message['mrkdwn_in'] = ['text']

        return message
