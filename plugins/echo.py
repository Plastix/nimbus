from plugin import CommandPlugin, PluginException


class Echo(CommandPlugin):
    """
    Basic Echo command
    """

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['echo']
        self.short_help = 'Repeat after me'
        self.help = 'Echos back whatever was said'
        self.help_example = ['!echo test']

    def on_command(self, event, response):
        args = event['text']
        if args:
            response['text'] = args
            self.bot.sc.api_call('chat.postMessage', **response)
        else:
            raise PluginException('Missing arguments. E.g. `!echo <text>`')
