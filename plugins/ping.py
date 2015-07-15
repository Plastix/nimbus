from plugin import CommandPlugin


class Ping(CommandPlugin):
    """
    Pong!
    """

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['ping']
        self.short_help = 'Pong!'
        self.help = self.short_help
        self.help_example = ['!ping']

    def on_command(self, bot, event, response):
        response.update(text='pong')
        bot.sc.api_call('chat.postMessage', **response)
