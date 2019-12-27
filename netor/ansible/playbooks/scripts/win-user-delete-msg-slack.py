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

print("sys.argv= " + str(sys.argv))

channel = sys.argv[-1]

# define user and server variables
if sys.argv[-2] == 'local':
    server = sys.argv[-3]
    user = sys.argv[-4]
    text = ""
elif sys.argv[-2] == 'ad':
    user = sys.argv[-3]
    server = ""
    text = ""
else:
    text = "Error:1 "
    user = ""
    server = ""

if ('was' in sys.argv) and ('not' in sys.argv) and (sys.argv[-2] == 'local'):
    text += "`Usuario \"{}\" no encontrado en el servidor \"{}\"`".format(user, server)
elif ('deleted' in sys.argv) and (sys.argv[-2] == 'local'):
    text += "```Usuario \"{}\" eliminado del servidor \"{}\"```".format(user, server)
elif ('absent' in str(sys.argv)) and (sys.argv[-2] == 'ad') and ('changed\': False' in str(sys.argv)):
    text += "`Usuario \"{}\" no encontrado en AD`".format(user)
elif ('absent' in str(sys.argv)) and (sys.argv[-2] == 'ad') and ('changed\': True' in str(sys.argv)):
    text += "```Usuario \"{}\" eliminado de AD```".format(user)
else:
    text += "Error:2"

client.api_call('chat.postMessage', channel=channel, text=text)
