import time
import re
from slackclient import SlackClient
import socket
import ipaddress
import subprocess

# instantiate Slack client
slack_client = SlackClient("YOUR-TOKEN-GOES-HERE")
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
_RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
_EXAMPLE_COMMAND = "do"
_MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
_PLAYBOOK_FULL_PATH_NAME = _NETOR_HOME_DIRECTORY + "netor/ansible/playbooks/"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(_MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def verify_source(source):
    with open(_NETOR_HOME_DIRECTORY + "netor/ansible/hosts", "r") as file:
        for line in file:
            if source in line:
                ansible_host = re.search("(.*) ansible_host", line)
                return ansible_host[1]
    return False


def fix_hostname(host):
    if "http" in host:
        host = re.search("\|(.*)>", host)
        return host[1]


def verify_host(host):
    try:
        ipaddress.ip_address(host)
    except ValueError:
        try:
            host = socket.gethostbyname(fix_hostname(host))
        except socket.error:
            return False
        except TypeError:
            return False
        else:
            return host
    else:
        return host


def send_msg(channel_sm, response_sm):
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_sm,
        text=response_sm
    )


def ansible_cmd(playbook, channel_hd, **kwargs):
    p_book = _PLAYBOOK_FULL_PATH_NAME + playbook
    cmd = "ansible-playbook " + p_book + " --extra-vars \""
    for key, value in kwargs.items():
        cmd += key + "=" + value + " "
    cmd += "\""

    send_msg(channel_hd, "Comando en ejecucion")
    subprocess.Popen(cmd, shell=True)


def win_ping(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    source = verify_source(command_hd_splited[1])
    destination = verify_host(command_hd_splited[2])
    if not source:
        send_msg(channel_hd, "*El origen no está en mi inventario de equipos*")
        return
    if not destination:
        send_msg(channel_hd, "*El destino es invalido*")
        return
    ansible_cmd("win-ping-msg-slack.yml", channel_hd, cmd="ping", source=source, destination=destination)


def list_inventory(channel_hd):
    text = ""
    with open(_NETOR_HOME_DIRECTORY + "netor/ansible/hosts", "r") as file:
        for line in file:
            match = re.search("(.*) ansible_host=([^\s]+)", line)
            if match:
                text += match[1] + " \t" + match[2] + "\n"
    send_msg(channel_hd, text)


def win_ver_usuario(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    user = command_hd_splited[1]
    ansible_cmd("win-user-view-msg-slack.yml", channel_hd, user=user)


def win_desbloquear_usuario(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    user = command_hd_splited[1]
    ansible_cmd("win-user-unlock-msg-slack.yml", channel_hd, user=user)


def win_deshabilitar_usuario(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    user = command_hd_splited[1]
    ansible_cmd("win-user-disable-msg-slack.yml", channel_hd, user=user)


def handle_command(command_hd, channel_hd):
    """
        Executes bot command if the command is known
    """

    if command_hd.startswith("help"):
        response = "Esta es la lista de commandos que puedes ejecutar:\n" \
                   "- @boty listar inventario \n" \
                   "- @boty win-ping _direccion_ip_origen_ _direccion_ip_destino_\n" \
                   "- @boty win-ver-usuario _user_id_\n" \
                   "- @boty win-desbloquear-usuario _id_de_usuario_\n" \
                   "- @boty win-deshabilitar-usuario _id_de_usuario_"
        send_msg(channel_hd, response)

    elif command_hd.startswith("win-ping"):
        win_ping(command_hd, channel_hd)

    elif command_hd.startswith("listar inventario"):
        list_inventory(channel_hd)

    elif command_hd.startswith("win-ver-usuario"):
        win_ver_usuario(command_hd, channel_hd)

    elif command_hd.startswith("win-desbloquear-usuario"):
        win_desbloquear_usuario(command_hd, channel_hd)

    elif command_hd.startswith("win-deshabilitar-usuario"):
        win_deshabilitar_usuario(command_hd, channel_hd)

    else:
        response = "No conozco ese comando. Intenta con *\"@boty help\"* para ver la lista de comandos."
        send_msg(channel_hd, response)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(_RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
