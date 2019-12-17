import sys
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

t = sys.argv

if ('Max'in t) and ('retries' in t) and ('exceeded') in t:
    t = "`Error de conexion al servidor o dispositivo de red`"
    client.api_call('chat.postMessage', channel='test2', text=t)