import sys
import ast
from slackclient import SlackClient

slack_token_slack = "xoxb-834321038834-869083359104-Cn2cHbJ6lBSC9jwTaSIQyYxg"
client = SlackClient(slack_token_slack)

# define user and server variables
if sys.argv[-1] == 'local':
    server = sys.argv[-2]
    user = sys.argv[-3]
    text = ""
elif sys.argv[-1] == 'ad':
    user = sys.argv[-2]
    server = ""
    text = ""
else:
    text = "Error:1 "
    user = ""
    server = ""

print("length sys.argv= " + str(len(sys.argv)))
print("type sys.argv= " + str(type(sys.argv)))
print("sys.argv= " + str(sys.argv))
print("user= " + user)
print("server= " + server)
print(sys.argv[-3])
if ('was' in sys.argv) and ('not' in sys.argv) and (sys.argv[-1] == 'local'):
    text += "`Usuario \"{}\" no encontrado en el servidor \"{}\"`".format(user, server)
elif ('deleted' in sys.argv) and (sys.argv[-1] == 'local'):
    text += "```Usuario \"{}\" eliminado del servidor \"{}\"```".format(user, server)
elif ('absent' in str(sys.argv)) and (sys.argv[-1] == 'ad') and ('changed\': False' in str(sys.argv)):
    text += "`Usuario \"{}\" no encontrado en AD`".format(user)
elif ('absent' in str(sys.argv)) and (sys.argv[-1] == 'ad') and ('changed\': True' in str(sys.argv)):
    text += "```Usuario \"{}\" eliminado de AD```".format(user)
else:
    text += "Error:2"

print("text= " + text)

client.api_call('chat.postMessage', channel='test2', text=text)
