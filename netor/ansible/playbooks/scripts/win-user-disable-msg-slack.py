import sys
from slackclient import SlackClient

slack_token_slack = "YOUR-TOKEN-GOES-HERE"
client = SlackClient(slack_token_slack)

s = sys.argv[1]

if "\'account_disabled\': True" in s:
    t = "*Se ha deshabilitado el usuario*"
else:
    t = "*El usuario no existe*"

client.api_call('chat.postMessage', channel='test2', text=t)
