import sys
import ast
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

s = sys.argv[1]

try:
    d = ast.literal_eval(s)
except SyntaxError:
    t = "`El usuario \"{}\" no existe`".format(sys.argv[2])
else:

    if d['state'] == 'absent':
        t = "`El usuario \"{}\" no existe`".format(sys.argv[2])
    else:
        if 'name' in d:
            name = str(d['name'])
        else:
            name = str(d['fullname'])

        if 'account_disabled' in d:
            account_disabled = str(d['account_disabled'])
        else:
            account_disabled = str(d['enabled'])

        if d['state'] == 'present':
            t = "```userID: " + str(d['name']) + "\n"
            t += "*fullname:* " + name + "\n"
            t += "*description:* " + str(d['description']) + "\n"
            t += "*account_disabled:* " + account_disabled + "\n"
            t += "*account_locked:* " + str(d['account_locked']) + "\n"
            t += "*password_expired:* " + str(d['password_expired']) + "\n"
            t += "*password_never_expires:* " + str(d['password_never_expires']) + "\n"
            t += "*user_cannot_change_password:* " + str(d['user_cannot_change_password']) + "\n"
            t += "*groups:* " + str(d['groups']) + "```\n"
        else:
            t = "`El usuario \"{}\" no existe`".format(sys.argv[2])

client.api_call('chat.postMessage', channel='test2', text=t)
