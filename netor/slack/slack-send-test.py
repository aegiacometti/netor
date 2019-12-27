from slackclient import SlackClient
import sys

slack_token = 'xxxx'
client = SlackClient(slack_token)
msg_test = sys.argv[1]


def send_msg(msg):
    client.api_call('chat.postMessage', channel="test2", as_user="true", text=msg)


if client.rtm_connect():
    msg = msg_test
    send_msg(msg)
else:
    print("Connection Failed")
