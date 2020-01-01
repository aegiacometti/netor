#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import time
import re
from slackclient import SlackClient
import subprocess
import configparser
# import slacklogging
import sys
from datetime import datetime
import traceback
import requests
import json
import os

# constants
_RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
_EXAMPLE_COMMAND = "do"
_MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
_NETOR_HOME_DIRECTORY = os.getenv('NETOR')
_ANSIBLE_INVENTORY_FULL_PATH_NAME = _NETOR_HOME_DIRECTORY + "netor/ansible/hosts"
_PLAYBOOK_FULL_PATH_NAME = _NETOR_HOME_DIRECTORY + "netor/ansible/playbooks/skynet/"
_BOT_CHANNEL = "skynet"
_BOT_NAMES_LIST = ['bot-ad', 'bot-win', 'bot-hhrr', 'bot-linux', 'bot-networking', 'bot-skynet']

# variables in files
_AUTHORIZATION_FILE_USERS = _NETOR_HOME_DIRECTORY + 'netor/slack/authorizations/auth-user-skynet.txt'
_AUTHORIZATION_FILE_BOT = _NETOR_HOME_DIRECTORY + 'netor/slack/authorizations/auth-bot-skynet.txt'

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)
bot_log_file = config['Slack']['bot_skynet_log_file']
bot_oauth_token = config['Slack']['bot_skynet_oauth']

# instantiate Slack client
slack_client = SlackClient(bot_oauth_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


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
                return message, event["channel"], str(event["user"])
    return None, None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(_MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def send_msg(channel_sm, response_sm):
    # Sends the response back to the channel
    try:
        slack_client.api_call("chat.postMessage", channel=channel_sm, text=response_sm)
    except Exception:
        log_msg("Send_msg(): Cannot send message to Slack.")
        log_exception()
    log_msg("Chat Response on Channel {}\n{}\n".format(channel_sm, response_sm))


def ansible_cmd(playbook, channel_hd, **kwargs):
    p_book = _PLAYBOOK_FULL_PATH_NAME + playbook
    cmd = "ansible-playbook " + p_book + " -i " + _ANSIBLE_INVENTORY_FULL_PATH_NAME + " --extra-vars \""
    for key, value in kwargs.items():
        cmd += key + "=" + value + " "
    cmd += "channel=" + _BOT_CHANNEL + "\" -vvvv"

    send_msg(channel_hd, "```Comando en ejecución```")
    log_msg("Ansible_CMD= " + cmd)

    subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)


def authorized_user(slack_user):
    file = open(_AUTHORIZATION_FILE_USERS, 'r')
    authorized_user_ids = file.read()
    file.close()
    if slack_user in authorized_user_ids:
        return True
    else:
        return False


def get_slack_user_name(slack_user_id):
    payload = {'token': bot_oauth_token, 'user': slack_user_id}
    response = requests.get('https://slack.com/api/users.info', params=payload)
    response_to_dict = json.loads(response.text)
    try:
        return response_to_dict['user']['name']
    except Exception:
        log_msg("get_slack_user_name(): Cannot get slack_user_id->user_name from Slack API.")
        log_exception()


def authorized_bot(slack_channel):
    file = open(_AUTHORIZATION_FILE_BOT, 'r')
    authorized_bot_ids = file.read()
    file.close()
    if slack_channel in authorized_bot_ids:
        return True
    else:
        return False


def view_bot_log(command_hd, channel_hd):
    command_hd_splited = command_hd.split()

    if len(command_hd_splited) < 2 or len(command_hd_splited) > 3:
        send_msg(channel_hd, "`Sintaxis incorrecta.`")
    elif command_hd_splited[1].lower() not in _BOT_NAMES_LIST:
        send_msg(channel_hd, "`Nombre de Bot incorrecto.`")
    else:
        try:
            log_lines = int(command_hd_splited[2])
            if log_lines > 2000:
                log_lines = 2000
        except IndexError:
            log_lines = 200
        except ValueError:
            log_lines = 200

        bot_log_file_name = 'slack-{}.log'.format(command_hd_splited[1].lower())

        log_file = _NETOR_HOME_DIRECTORY + 'netor/log/{}'.format(bot_log_file_name)

        cmd = 'tail -{} {}'.format(log_lines, log_file)
        send_msg(channel_hd, "```Comando en ejecución```")
        log_msg("CMD= " + cmd)

        output = subprocess.run(cmd, shell=True, universal_newlines=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_text = output.stderr + "\n" + output.stdout
        send_msg(channel_hd, output_text)


def bot_command(command_hd, channel_hd):
    command_hd_splited = command_hd.split()

    if len(command_hd_splited) != 3:
        send_msg(channel_hd, "`Sintaxis incorrecta.`")
    elif command_hd_splited[1].lower() not in _BOT_NAMES_LIST:
        send_msg(channel_hd, "`Nombre de Bot incorrecto.`")
    elif command_hd_splited[2] not in ['start', 'stop', 'restart', 'status']:
        send_msg(channel_hd, "`Sintaxis incorrecta.`")
    else:
        send_msg(channel_hd, "```Comando en ejecución```")

        cmd = 'sudo /usr/sbin/service slack-{} {}'.format(command_hd_splited[1], command_hd_splited[2])
        log_msg("CMD= " + cmd)
        output_cmd = subprocess.run(cmd, shell=True, universal_newlines=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_text = output_cmd.stderr + "\n" + output_cmd.stdout
        send_msg(channel_hd, output_text)

        if command_hd_splited[2] != 'status':
            cmd_status = 'sudo /usr/sbin/service slack-{} status'.format(command_hd_splited[1])
            log_msg("CMD= " + cmd_status)
            output_status = subprocess.run(cmd_status, shell=True, universal_newlines=True,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_text = output_status.stderr + "\n" + output_status.stdout
            send_msg(channel_hd, output_text)


def git_pull_updates(channel_hd):
    send_msg(channel_hd, "```Comando en ejecución```")
    cmd = 'git --git-dir={}.git --work-tree={} pull origin master'.format(_NETOR_HOME_DIRECTORY, _NETOR_HOME_DIRECTORY)
    output_cmd = subprocess.run(cmd, shell=True, universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_text = output_cmd.stderr + "\n" + output_cmd.stdout
    send_msg(channel_hd, output_text)


def handle_command(command_hd, channel_hd):
    """
        Executes bot command if the command is known
    """

    if command_hd.startswith("help"):
        response = "```Esta es la lista de commandos que puedes ejecutar:\n" \
                   "- @Bot-Skynet ver-bot-log botname(without @) (opcional #lineas, def: 200 max:2000)\n" \
                   "- @Bot-Skynet bot botname(without @) restart\start\stop\status \n" \
                   "- @Bot-Skynet git pull updates```"
        send_msg(channel_hd, response)

    elif command_hd.startswith("ver-bot-log "):
        view_bot_log(command_hd, channel_hd)

    elif command_hd.startswith("bot "):
        bot_command(command_hd, channel_hd)

    elif command_hd == "git pull updates":
        git_pull_updates(channel_hd)

    else:
        response = "`No conozco ese comando. Intenta con \"@Skynet help\" para ver la lista de comandos.`"
        send_msg(channel_hd, response)


def log_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
    sys.stdout.flush()


def log_msg(msg):
    now = datetime.now()
    dt_string = now. strftime("%d/%m/%Y %H:%M:%S")
    print("{} - {}".format(dt_string, msg))
    sys.stdout.flush()
    # slacklogging.log_msg(bot_log_file, __file__, msg)


if __name__ == "__main__":
    sys.stdout = open(bot_log_file, '+a')

    if slack_client.rtm_connect(with_team_state=False):
        log_msg("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            try:
                command, channel, slack_userid = parse_bot_commands(slack_client.rtm_read())
            except Exception:
                log_msg("main(): Cannot send message to Slack.")
                log_exception()
                log_msg("main(): Restarting connection with Slack.")
                time.sleep(5)
                slack_client.rtm_connect(with_team_state=False)
            else:
                if command:
                    user_auth_status = authorized_user(slack_userid)
                    bot_auth_status = authorized_bot(channel)
                    log_msg("UserID= {} - Command= {} - Channel= {} - Authorized= {}".format(slack_userid, command,
                                                                                             channel, user_auth_status))
                    if user_auth_status and bot_auth_status:
                        handle_command(command, channel)
                    elif user_auth_status and not bot_auth_status:
                        send_msg(channel, "`\"Bot\" no autorizado a recibir comandos en este canal`")
                    else:
                        username = get_slack_user_name(slack_userid)
                        send_msg(channel, "`Usuario \"{}\" ID \"{}\" no autorizado"
                                          " a ejecutar el comando`".format(username, slack_userid))

            time.sleep(_RTM_READ_DELAY)
    else:
        log_msg("Connection failed. Exception traceback printed above.")
