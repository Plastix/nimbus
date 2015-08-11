import random
from plugin import CommandPlugin, PluginException


class CoinFlip(CommandPlugin):
    """
    Flip a coin
    """
    max_coin_flips = 1000000

    def __init__(self, bot):
        CommandPlugin.__init__(self, bot)
        self.triggers = ['coin', 'coinflip']
        self.short_help = 'Flip a coin'
        self.help = 'Flip a coin or number of coins'
        self.help_example = ['!coin', '!coinflip 5']

    def on_command(self, event, response):
        args = event['text']

        if not args:
            response['text'] = 'A coin is flipped and it is *_%s_*!' % random.choice(['Heads', 'Tails'])
        else:
            try:
                tosses = int(args)
                if tosses <= 0:
                    raise PluginException('Invalid argument! No coins to flip!')

                # Avoid taking too long to generate coin flips
                if tosses > CoinFlip.max_coin_flips:
                    raise PluginException(
                        'Invalid argument! Number of coins to flip is too large! Max flips is `%s`.' % CoinFlip.max_coin_flips)

                rand_bits = bin(random.getrandbits(tosses))[2:]
                heads = rand_bits.count('0')
                tails = tosses - heads
                response['text'] = '*_%s_* coins are flipped and the result is *_%s Heads_* and *_%s Tails_*!' % (
                    tosses, heads, tails)
            except ValueError:
                raise PluginException('Invalid argument! Specify a *number* of coins to flip. E.g. `!coin 5`')

        response['mrkdwn_in'] = ['text']
        self.bot.sc.api_call('chat.postMessage', **response)
