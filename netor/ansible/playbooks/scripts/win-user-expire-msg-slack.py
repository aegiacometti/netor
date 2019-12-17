import sys
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

s = sys.argv[1]
u = sys.argv[2]

if "\'password_expired\': True" in s:
    t = "```Se ha expirado la password del usuario \"{}\". Debe cambiarla al proximo login.```".format(u)
else:
    t = "`El usuario \"{}\" no existe`".format(u)

client.api_call('chat.postMessage', channel='test2', text=t)
