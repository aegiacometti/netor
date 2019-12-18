import sys
from slackclient import SlackClient
import configparser

print("sys.argv= " + str(sys.argv))

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = "../../netor.config"
config.read(netor_config_path_name)
bot_ad_oauth_token = config['Slack']['bot_ad_oauth']

client = SlackClient(bot_ad_oauth_token)

t = sys.argv

print("Text= " + str(t))

if ('Max'in t) and ('retries' in t) and ('exceeded') in t:
    t = "`Error de conexion al servidor o dispositivo de red`"
    client.api_call('chat.postMessage', channel='activedirectory', text=t)
