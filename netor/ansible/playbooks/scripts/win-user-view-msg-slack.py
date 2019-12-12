import sys
import ast
from slackclient import SlackClient

slack_token_slack = "YOUR-TOKEN-GOES-HERE"
client = SlackClient(slack_token_slack)

s = sys.argv[1]

try:
    d = ast.literal_eval(s)
except SyntaxError:
    t = "*El usuario no existe*"
else:
    if d['state'] == 'present':
        t = "*name:* " + str(d['name']) + "\n"
        t += "*fullname:* " + str(d['fullname']) + "\n"
        t += "*description:* " + str(d['description']) + "\n"
        t += "*account_disabled:* " + str(d['account_disabled']) + "\n"
        t += "*account_locked:* " + str(d['account_locked']) + "\n"
        t += "*password_expired:* " + str(d['password_expired']) + "\n"
        t += "*password_never_expires:* " + str(d['password_never_expires']) + "\n"
        t += "*user_cannot_change_password:* " + str(d['user_cannot_change_password']) + "\n"
        t += "*groups:* " + str(d['groups']) + "\n"
    else:
        t = "*El usuario no existe*"

client.api_call('chat.postMessage', channel='test2', text=t)
