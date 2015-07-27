import json
from plugin import CommandPlugin
import requests
from utils import get_urls


class IsUp(CommandPlugin):
    """
    Command for checking if a website is offline
    """

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['isup', 'isonline']
        self.short_help = 'Pings a website to check if it is online'
        self.help = self.short_help
        self.help_example = ['!isup google.com', '!isup oc.tc']

    def on_command(self, bot, event, response):
        text = event['text']
        if text:
            urls = get_urls(text)
            for url in urls:
                resp = dict(response)
                resp.update(attachments=json.dumps([IsUp.is_up(url)]))
                bot.sc.api_call('chat.postMessage', **resp)

    @staticmethod
    def is_up(url):

        attachment = {
            'title': 'Is Website Up? (%s)' % url,
            'mrkdwn_in': ['text']
        }

        # Catch any requests errors if any
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                attachment['text'] = ":white_check_mark: Looks up from here!"
            else:
                attachment['text'] = ':warning: Issue from here! (Error %s)' % r.status_code

        except Exception as e:
            attachment['text'] = ':x: Error checking website! (Error %s)' % e.__class__.__name__

        return attachment
