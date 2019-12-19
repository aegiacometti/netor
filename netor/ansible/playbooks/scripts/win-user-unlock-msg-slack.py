import sys
from slackclient import SlackClient
import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_ad_oauth_token = config['Slack']['bot_ad_oauth']

client = SlackClient(bot_ad_oauth_token)

s = sys.argv[1]
channel = sys.argv[-1]

print("sys.argv= " + str(sys.argv))

if ("\'account_locked\': False" in s) and ("\'changed\': False" in s):
    t = "`El usuario \"{}\" no estaba bloqueado`".format(sys.argv[2])
elif ("\'account_locked\': False" in s) and ("\'changed\': True" in s):
    t = "```Se ha desbloqueado el usuario \"{}\"```".format(sys.argv[2])
else:
    t = "`El usuario no existe`"

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)
