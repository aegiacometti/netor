import sys
import ast
from slackclient import SlackClient
import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_ad_oauth_token = config['Slack']['bot_ad_oauth']

client = SlackClient(bot_ad_oauth_token)

s = sys.argv[1]
u = sys.argv[-3]
g = sys.argv[-2]
channel = sys.argv[-1]

print("sys.argv= " + str(sys.argv))

if "Conditional result was False" in s:
    t = "`El usuario \"" + u + "\" no existe`"
else:
    try:
        d = ast.literal_eval(s)
    except SyntaxError:
        t = "`El grupo \"" + g + "\" no existe`"
    else:
        if 'msg' in d:
            msg = str(d['msg'])
            if msg.startswith("Could not find domain user"):
                t = "`El usuario \"" + u + "\" o el grupo \"" + g + "\" no existe`"
            else:
                t = "`Error:1 de formato de respuesta del servidor`"
        else:
            added = str(d['added'])
            changed = str(d['changed'])
            members = str(d['members'])
            removed = str(d['members'])
            if changed == "False" and u in members:
                t = "`El usuario \"" + u + "\" ya estaba en el grupo \"" + g + "\"`"
            elif changed == "False" and u not in members:
                t = "`El usuario \"" + u + "\" no estaba en el grupo \"" + g + "\"`"
            elif changed == "True" and u in members:
                t = "```El usuario \"" + u + "\" se agrego al grupo \"" + g + "\"```"
            else:
                t = "```El usuario \"" + u + "\" se quito en el grupo \"" + g + "\"```"

print("Text= " + t)

client.api_call('chat.postMessage', channel=channel, text=t)
