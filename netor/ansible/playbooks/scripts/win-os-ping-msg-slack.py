import sys
from slackclient import SlackClient
import configparser

print("sys.argv= " + str(sys.argv))

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_win_oauth_token = config['Slack']['bot_win_oauth']

client = SlackClient(bot_win_oauth_token)

t = "```" + sys.argv[1] + "```"
channel = sys.argv[-1]

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)

