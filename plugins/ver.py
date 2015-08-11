import subprocess
from metadata import version, url
from plugin import CommandPlugin
from utils import is_git_directory


class Ver(CommandPlugin):
    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['ver', 'version', 'about']
        self.short_help = 'Prints out version information about the bot'
        self.help = self.short_help
        self.help_example = ['!ver']

    def on_command(self, event, response):
        ver = version
        if is_git_directory():
            ver = '%s (%s)' % (version, Ver.get_git_revision_short_hash())

        response['text'] = '_Nimbus version_ `%s`\n%s\n' % (ver, url)
        response['mrkdwn_in'] = ['text']
        self.bot.sc.api_call('chat.postMessage', **response)

    @staticmethod
    def get_git_revision_short_hash():
        """
        Returns the current SHA hash of the git repo. Only works if the current path is a git repo.
        Call utils.is_git_directory to make sure
        """
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
