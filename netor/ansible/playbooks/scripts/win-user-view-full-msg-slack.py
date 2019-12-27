import sys
import ast
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
channel = sys.argv[-1]
user = sys.argv[-2]

print("sys.argv= " + str(sys.argv))

try:
    d = ast.literal_eval(s)
except SyntaxError:
    t = "`El usuario \"{}\" no existe`".format(user)
else:

    if d['state'] == 'absent':
        t = "`El usuario \"{}\" no existe`".format(user)
    else:
        if 'name' in d:
            name = str(d['name'])
        else:
            name = str(d['fullname'])

        if 'account_disabled' in d:
            account_disabled = str(d['account_disabled'])
        else:
            account_disabled = str(d['enabled'])

        if d['state'] == 'present':
            t = "```userID: " + str(d['name']) + "\n"
            t += "*fullname:* " + name + "\n"
            t += "*description:* " + str(d['description']) + "\n"
            t += "*account_disabled:* " + account_disabled + "\n"
            t += "*account_locked:* " + str(d['account_locked']) + "\n"
            t += "*password_expired:* " + str(d['password_expired']) + "\n"
            t += "*password_never_expires:* " + str(d['password_never_expires']) + "\n"
            t += "*user_cannot_change_password:* " + str(d['user_cannot_change_password']) + "\n"
            t += "*groups:* " + str(d['groups']) + "```\n"
        else:
            t = "`El usuario \"{}\" no existe`".format(user)

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)
