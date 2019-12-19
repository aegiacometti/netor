import sys
from slackclient import SlackClient
import configparser


print("sys.argv= " + str(sys.argv))

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_win_webhook_token = config['Slack']['bot_win_webhook']

client = SlackClient(bot_win_webhook_token)

t = sys.argv
channel = sys.argv[-1]

print("Text= " + str(t))

if ('Max'in t) and ('retries' in t) and ('exceeded') in t:
    t = "`Error de conexion al servidor o dispositivo de red`"
    client.api_call('chat.postMessage', channel='windows', text=t)
