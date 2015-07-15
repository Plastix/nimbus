from metadata import version, url
from plugin import CommandPlugin


class Ver(CommandPlugin):
    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['ver', 'version', 'about']
        self.short_help = 'Prints out version information about the bot'
        self.help = self.short_help
        self.help_example = ['!ver']

    def on_command(self, bot, event, response):
        response['text'] = 'Nimbus version `%s`\n%s' % (version, url)
        response['mrkdwn_in'] = ['text']
        bot.sc.api_call('chat.postMessage', **response)
