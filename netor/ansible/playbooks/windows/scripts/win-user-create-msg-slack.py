import sys
from slackclient import SlackClient
import configparser
import os

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = os.getenv('NETOR')
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_ad_oauth_token = config['Slack']['bot_ad_oauth']

client = SlackClient(bot_ad_oauth_token)

s = sys.argv[1]
u = sys.argv[-2]
scope = sys.argv[-3]

channel = sys.argv[-1]

print("sys.argv= " + str(sys.argv))

if 'Conditional result was False' in s:
    t = "`El usuario \"{}\" ya existe en \"{}\"`".format(u, scope)
elif u in s:
    t = "```Se ha creado el usuario \"{}\" en \"{}\"```".format(u, scope)
else:
    t = '`Error`'

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)
