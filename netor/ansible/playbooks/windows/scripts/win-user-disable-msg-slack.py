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

s = str(sys.argv)
channel = sys.argv[-2]
user = sys.argv[-1]
print(type(s))
print("sys.argv= " + str(sys.argv))

if ("\'account_disabled\': True" in s) and ("\'changed\': True" in s):
    t = "```Se ha deshabilitado el usuario \"{}\"```".format(user)
elif ("\'account_disabled\': True" in s) and ("\'changed\': False" in s):
    t = "`El usuario \"{}\" ya estaba deshabilitado`".format(user)
else:
    t = "`El usuario \"{}\" no existe`".format(user)

print("Text= " + t)
print(user)
print(channel)
client.api_call('chat.postMessage', channel=channel, text=t)
