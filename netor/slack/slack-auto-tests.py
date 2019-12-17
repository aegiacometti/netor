from slackclient import SlackClient
import sys
import time

slack_token = "xoxp-834321038834-848962750199-874165795600-db097ce14d3cbc02f92ae4096ea6197c"
client = SlackClient(slack_token)

try:
    test_number = sys.argv[1]
except Exception:
    test_number = 'all'


def send_msg(msg):
    client.api_call('chat.postMessage', channel="test2", as_user="true", text=msg)


x = 1
if client.rtm_connect():
    with open("./tests.txt", "r") as file:

        if test_number == 'all':
            for line in file:
                print("Test #" + str(x) + " - Comando= " + line)
                send_msg(line)
                if "#" in line:
                    time.sleep(2)
                else:
                    x += 1
                    time.sleep(20)
else:
    print("Connection Failed")
