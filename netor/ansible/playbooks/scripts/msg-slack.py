import sys
import ast

from slackclient import SlackClient

slack_token_slack = "YOUR-TOKEN-GOES-HERE"
client = SlackClient(slack_token_slack)

text = str(sys.argv[1])

client.api_call('chat.postMessage', channel='test', text=text)
