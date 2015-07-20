from plugin import CommandPlugin
from utils import strip_url_formatting
import minecraft.ping
import json


class MCPing(CommandPlugin):
    """
    Ping a Minecraft server
    """
    default_server_port = 25565

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['mcping', 'mcp']
        self.short_help = 'Ping a Minecraft server'
        self.help = self.short_help
        self.help_example = ['!mcping us.oc.tc', '!mcping example.org:1234']

    def on_command(self, bot, event, response):
        args = event['text']
        if args:
            split = args.split(' ', 1)
            attach = MCPing.ping_mc_server(split[0])
            response.update(attachments=json.dumps([attach]))
            bot.sc.api_call('chat.postMessage', **response)

    @staticmethod
    def build_slack_attachment(server_address, data):

        attach = {'text': '', 'mrkdwn_in': ['text'], 'color': 'good',
                  'title': 'Minecraft Server Ping: %s' % server_address}

        attach['text'] += '*Online Players:* `%s/%s`\n' % (data['players']['online'], data['players']['max'])
        attach['text'] += '*Latency:* `%sms`\n' % data['ping']
        attach['text'] += '*Version:* `%s`\n' % data['version']['name']

        return attach

    # noinspection PyBroadException
    @staticmethod
    def ping_mc_server(args):
        raw = strip_url_formatting(args)
        server_address = raw
        port = MCPing.default_server_port

        parts = raw.split(':')
        # Set port if specified
        if len(parts) > 1:
            server_address = parts[0]
            port = parts[1]

        try:
            response = minecraft.ping.get_info(server_address, port)
        except:
            return {
                'title': 'Unable to ping Minecraft server: %s:%s!' % (server_address, port),
                'color': 'danger'
            }

        return MCPing.build_slack_attachment(server_address, response)
