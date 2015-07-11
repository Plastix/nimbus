#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Slack bot for Overcast Network """

import sys
import time

import yaml
from slackclient import SlackClient

from link_expander import expand_links


def get_config(filename):
    """ get Slack API token from config file """
    try:
        return yaml.safe_load(file(filename))
    except IOError as e:
        print("Couldn't open configuration file: %s" % e)


def process_message(text, content, sc):
    """ main processing function

        put all of the decisiony stuff in here as functionality is added
    """
    if 'oc.tc/' in text:
        expand_links(text, content, sc)


def main(filename):
    """ run main loop to listen for messages """
    config = get_config(filename)
    username = config.get('username', 'nimbus')
    icon_emoji = config.get('icon_emoji', 'cloud')
    icon_emoji = ':' + icon_emoji + ':'
    polling_interval = config.get('polling_interval', 1)
    token = config.get('token')

    if not token:
        print('Need an authorization token.')
        return

    sc = SlackClient(token)
    if not sc.rtm_connect():
        print("Can't connect to Slack.")
        return

    while True:
        events = sc.rtm_read()
        for event in events:
            if 'type' in event and event['type'] == 'message':
                if 'username' == username or 'attachments' in event.keys():
                    continue

                # base content shared by all bot actions
                content = dict(channel=event['channel'], username=username, icon_emoji=icon_emoji)
                text = event['text']
                process_message(text, content, sc)

        time.sleep(polling_interval)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        config_filename = sys.argv[1]
        main(config_filename)
    else:
        print('Please include the name of a configuration file')
