from slackclient import SlackClient
import sys
import time

test_file = sys.argv[1]

slack_token = 'xxxx'
client = SlackClient(slack_token)

try:
    test_number = sys.argv[1]
except Exception:
    test_number = 'all'


def send_msg(msg, channel):
    client.api_call('chat.postMessage', channel=channel, as_user="true", text=msg)


x = 1
if client.rtm_connect():
    with open(test_file, "r") as file:

        if test_number == 'all':
            for line in file:
                print("Test #" + str(x) + " - Comando= " + line)
                if "AD" in test_file:
                    send_msg(line, channel='activedirectory')
                if "Win" in test_file:
                    send_msg(line, channel='windows')
                if "HHRR" in test_file:
                    send_msg(line, channel='hhrr')
                if "#" in line:
                    time.sleep(2)
                else:
                    x += 1
                    time.sleep(20)
else:
    print("Connection Failed")
