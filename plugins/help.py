from plugin import CommandPlugin, PluginException


class Help(CommandPlugin):
    """
    Command for viewing other bot commands
    """

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['help', 'h']
        self.help = 'Lookup information about bot commands'
        self.help_example = ['!help', '!help <command>']
        self.hidden = True
        self.dm_sender = True

    def on_command(self, bot, event, response):
        args = event['text']
        # If argument print out extended help page about command (if there is one)
        if args:
            command = bot.get_command(args)
            if command:
                text = '*Help for _%s_:*\n' % args
                if command.help:
                    text += command.help + '\n'

                text += '*Trigger Keyword(s):*\n'
                for trigger in command.triggers:
                    text += '`%s` ' % trigger
                text += '\n'

                if command.help_example:
                    text += '*Ex:* '
                    for example in command.help_example:
                        text += '`%s` ' % example

            else:
                raise PluginException('Unknown command named `%s`!' % args)

        # If no args print out full command list
        else:
            text = '*Available Commands:* (Type `!help <command>` for more info about a certain command).\n'
            for plugin in sorted(list(bot.plugins)):
                if isinstance(plugin, CommandPlugin) and not plugin.hidden:
                    text += '`%s%s` - %s\n' % (bot.command_prefix, plugin.triggers[0], plugin.short_help)

        response['text'] = text
        response['mrkdwn_in'] = ['text']
        bot.sc.api_call('chat.postMessage', **response)
