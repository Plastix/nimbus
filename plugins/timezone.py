from datetime import datetime
import json
import pytz as pytz
from plugin import CommandPlugin, PluginException


class TimeZone(CommandPlugin):
    """
    Converts a time to the timezones of the team members in the Slack team
    """

    def __init__(self):
        CommandPlugin.__init__(self)
        self.triggers = ['timezone', 'tz']

        self.timezones = set()

    def on_command(self, bot, event, response):
        args = event['text']

        response['text'] = '_Time Now:_ '
        response['mrkdwn_in'] = ['text']

        self.get_team_timezones(bot)

        localFormat = "%X%p *%Z*"
        utcmoment_unaware = datetime.utcnow()
        utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)

        local = list()
        for tz in self.timezones:
            localDatetime = utcmoment.astimezone(pytz.timezone(tz))
            local.append(localDatetime.strftime(localFormat))
        response['text'] += ', '.join(local)

        bot.sc.api_call('chat.postMessage', **response)

    def get_team_timezones(self, bot):
        """
        Gets all the timezones for the members of the Slack Team
        """
        team_members = json.loads(bot.sc.api_call('users.list'))
        if team_members.get('ok'):
            for member in team_members['members']:
                # Don't look at disabled users
                if member.get('deleted'):
                    continue

                if 'tz' in member and member['tz']:
                    self.timezones.add(member['tz'])

        if not self.timezones:
            raise PluginException('Team members don\'t have any time zones set!')
