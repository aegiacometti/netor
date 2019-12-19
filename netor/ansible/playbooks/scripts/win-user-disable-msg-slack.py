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
channel = sys.argv[-2]
user = sys.argv[-1]

print("sys.argv= " + str(sys.argv))

if ("\'account_disabled\': True" in s) and ("changed\': True"):
    t = "```Se ha deshabilitado el usuario \"{}\"```".format(user)
elif ("\'account_disabled\': True" in s) and ("changed\': False"):
    t = "```El usuario \"{}\" ya estaba deshabilitado```".format(user)
else:
    t = "`El usuario \"{}\" no existe`".format(user)

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)
