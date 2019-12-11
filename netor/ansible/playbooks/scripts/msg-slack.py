import sys

from slackclient import SlackClient

#slack_token = os.environ["TQJ9F14QJ/BQRHDS8E5/pc2ij5CLgGZkjiJityhUuqc5"]
#client = SlackClient(slack_token)

text = str(sys.argv)

print(text)

#client.api_call('chat.postMessage', channel='test', text=text)
