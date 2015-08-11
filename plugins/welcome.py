import json
from plugin import Plugin


class Welcome(Plugin):
    """
    Welcomes new members when they join the Slack team
    """

    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.event_type = 'team_join'

    def on_event(self, event, response):
        # Get list of all channels (don't include archived channels)
        channel_response = self.bot.sc.api_call('channels.list', **{'exclude_archived': 1})
        # Convert string response to JSON
        channel_response = json.loads(channel_response)

        # Find general channel
        general_channel = None
        if channel_response.get('ok'):
            for channel in channel_response['channels']:
                if channel.get('is_general'):
                    general_channel = channel['id']

        # Post welcome to general channel if one found
        if general_channel:
            user = event['user']['id']
            response['channel'] = general_channel
            response['link_names'] = 1  # Enables linking of names
            response['text'] = 'Welcome to the Slack team <@%s>!' % user
            self.bot.sc.api_call('chat.postMessage', **response)
