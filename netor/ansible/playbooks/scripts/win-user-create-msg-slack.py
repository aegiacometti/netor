import sys
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

s = sys.argv[1]
u = sys.argv[2]
scope = sys.argv[-1]

print("SSSSSSSSSS= " + s)
if 'Conditional result was False' in s:
    t = "`El usuario \"{}\" ya existe en \"{}\"`".format(u, scope)
elif u in s:
    t = "```Se ha creado el usuario \"{}\" en \"{}\"```".format(u, scope)
else:
    t = '`Error`'

client.api_call('chat.postMessage', channel='test2', text=t)
