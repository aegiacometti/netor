import sys
import ast
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

t = "```" + sys.argv[1] + "```"

client.api_call('chat.postMessage', channel='test2', text=t)
