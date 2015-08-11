import datetime
from plugin import CommandPlugin
import time


class Uptime(CommandPlugin):
    """
    Command for printing Uptime of Bot
    """

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['uptime']
        self.short_help = 'Prints out the uptime of the bot'
        self.help = self.short_help
        self.help_example = ['!uptime']

    def on_command(self, event, response):
        args = event['text']
        if not args:
            uptime = time.time() - self.bot.start_time
            uptime = datetime.timedelta(seconds=int(uptime))

            response.update(
                {
                    'text': 'Bot Uptime: `%s`' % uptime,
                    'mrkdwn_in': ['text']

                }
            )

            self.bot.sc.api_call('chat.postMessage', **response)
