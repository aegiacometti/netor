import sys
from slackclient import SlackClient
import configparser

print("sys.argv= " + str(sys.argv))

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = "../../netor.config"
config.read(netor_config_path_name)
bot_win_oauth_token = config['Slack']['bot_win_oauth']

client = SlackClient(bot_win_oauth_token)

t = "```" + sys.argv[1] + "```"

print("Text= " + t)

client.api_call('chat.postMessage', channel='windows', text=t)

