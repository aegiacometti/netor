import sys
import ast

from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-849046616935-UuWCCQcdoZ51sXlh3NrLCysL"
client = SlackClient(slack_token_slack)

text = str(sys.argv[1])

client.api_call('chat.postMessage', channel='test', text=text)
