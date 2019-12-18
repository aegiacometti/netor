import sys
from slackclient import SlackClient
import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = "../../netor.config"
config.read(netor_config_path_name)
bot_ad_oauth_token = config['Slack']['bot_ad_oauth']

client = SlackClient(bot_ad_oauth_token)

print("sys.argv= " + str(sys.argv))

s = sys.argv[1]
u = sys.argv[2]

if "\'password_expired\': True" in s:
    t = "```Se ha expirado la password del usuario \"{}\". Debe cambiarla al proximo login.```".format(u)
else:
    t = "`El usuario \"{}\" no existe`".format(u)

print("Text= " + t)

client.api_call('chat.postMessage', channel='activedirectory', text=t)
