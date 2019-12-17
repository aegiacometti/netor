import sys
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

s = sys.argv[1]

if "\'account_disabled\': True" in s:
    t = "```Se ha deshabilitado el usuario```"
else:
    t = "`El usuario no existe`"

client.api_call('chat.postMessage', channel='test2', text=t)
