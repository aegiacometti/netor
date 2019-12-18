#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import time
import re
from slackclient import SlackClient
import socket
import ipaddress
import subprocess
import configparser
import slacklogging
import sys

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = "../netor.config"
config.read(netor_config_path_name)

bot_oauth_token = config['Slack']['bot_ad_oauth']

# instantiate Slack client
slack_client = SlackClient(bot_oauth_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
_RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
_EXAMPLE_COMMAND = "do"
_MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
_PLAYBOOK_FULL_PATH_NAME = _NETOR_HOME_DIRECTORY + "netor/ansible/playbooks/"

# variables in files
_AUTHORIZATION_FILE = 'authorizations/auth-bot-ad.txt'


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


def verify_source(source):
    with open(_NETOR_HOME_DIRECTORY + "netor/ansible/hosts", "r") as file:
        source += " "
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
    try:
        slack_client.api_call("chat.postMessage", channel=channel_sm, text=response_sm)
    except Exception:
        slacklogging.log_msg(bot_log_file, __file__, "Cannot send message to Slack.")
        slacklogging.log_msg(bot_log_file, __file__, Exception)
    slacklogging.log_msg(bot_log_file, __file__, "Chat Command: " + response_sm + " - On Channel: " + channel_sm)


def ansible_cmd(playbook, channel_hd, **kwargs):
    p_book = _PLAYBOOK_FULL_PATH_NAME + playbook
    cmd = "ansible-playbook " + p_book + " --extra-vars \""
    for key, value in kwargs.items():
        cmd += key + "=" + value + " "
    cmd += "\" -vvvv"

    send_msg(channel_hd, "```Comando en ejecución```")
    slacklogging.log_msg(bot_log_file, __file__, "Ansible command: " + cmd)
    subprocess.Popen(cmd, shell=True)


def win_ver_usuario_basico(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    print(command_hd_splited)

    if str(command_hd_splited[1]).lower() == 'local':
        if len(command_hd_splited) == 4:
            server = verify_source(command_hd_splited[3])
            if not server:
                print("Server: {} no encontrado en el inventario".format(command_hd_splited[3]))
                send_msg(channel_hd,
                         "`El servidor \"{}\" no está en mi inventario de equipos`".format((command_hd_splited[3])))
                return
            else:
                print("Server: {} encontrado en el inventario".format(server))
                ansible_cmd("win-user-view-local-basic-msg-slack.yml", channel_hd, user=command_hd_splited[2],
                            server=server)
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, falta usuario o servidor`")
            return
    elif str(command_hd_splited[1]).lower() == 'ad':
        if len(command_hd_splited) == 3:
            ansible_cmd("win-user-view-ad-basic-msg-slack.yml", channel_hd, user=command_hd_splited[2])
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, falta usuario o servidor`")
            return
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"AD\"`")
        return


def win_ver_usuario_full(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    print(command_hd_splited)

    if str(command_hd_splited[1]).lower() == 'local':
        if len(command_hd_splited) == 4:
            server = verify_source(command_hd_splited[3])
            if not server:
                print("Server: {} no encontrado en el inventario".format(command_hd_splited[3]))
                send_msg(channel_hd,
                         "`El servidor \"{}\" no está en mi inventario de equipos`".format((command_hd_splited[3])))
                return
            else:
                print("Server: {} encontrado en el inventario".format(server))
                ansible_cmd("win-user-view-local-full-msg-slack.yml", channel_hd, user=command_hd_splited[2],
                            server=server)
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, falta usuario o servidor`")
            return
    elif str(command_hd_splited[1]).lower() == 'ad':
        if len(command_hd_splited) == 3:
            ansible_cmd("win-user-view-ad-full-msg-slack.yml", channel_hd, user=command_hd_splited[2])
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, falta usuario o servidor`")
            return
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"AD\"`")
        return


def win_desbloquear_usuario(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    server = ""
    if len(command_hd_splited) < 3:
        send_msg(channel_hd, "`Sintaxis incorrecta`")
        return
    else:
        user = command_hd_splited[2]

    if len(command_hd_splited) == 4:
        server = command_hd_splited[3]

    if str(command_hd_splited[1]).lower() == "local":
        ansible_cmd("win-user-unlock-local-msg-slack.yml", channel_hd, user=user, server=server)
    elif str(command_hd_splited[1]).lower() == "ad":
        ansible_cmd("win-user-unlock-ad-msg-slack.yml", channel_hd, user=user)
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"ad\" usuario`")
        return


def win_deshabilitar_usuario(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    user = command_hd_splited[2]
    server = ""

    if len(command_hd_splited) < 3:
        send_msg(channel_hd, "`Sintaxis incorrecta`")
        return

    if len(command_hd_splited) == 4:
        server = command_hd_splited[3]

    if str(command_hd_splited[1]).lower() == 'local':
        ansible_cmd("win-user-disable-local-msg-slack.yml", channel_hd, user=user, server=server)

    elif str(command_hd_splited[1]).lower() == 'ad':
        ansible_cmd("win-user-disable-ad-msg-slack.yml", channel_hd, user=user)
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"AD\"`")
        return


def win_usuario_grupo(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    server = ""
    if len(command_hd_splited) < 5:
        send_msg(channel_hd, "`Sintaxis incorrecta`")
        return
    else:
        user = command_hd_splited[3]
        group = command_hd_splited[4]

    if len(command_hd_splited) == 6:
        server = command_hd_splited[5]

    if str(command_hd_splited[2]).lower() == "agregar":
        state = "present"
    elif str(command_hd_splited[2]).lower() == "quitar":
        state = "absent"
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"agregar\" o \"quitar\" usuario`")
        return

    if str(command_hd_splited[1]).lower() == "local":
        ansible_cmd("win-user-group-local-msg-slack.yml", channel_hd, user=user, group=group,
                    state=state, server=server)
    elif str(command_hd_splited[1]).lower() == "ad":
        ansible_cmd("win-user-group-ad-msg-slack.yml", channel_hd, user=user, group=group, state=state)
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son local/ad usuario`")
        return


def win_usuario_cambiar_password(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    user = command_hd_splited[2]

    if str(command_hd_splited[1]).lower() == 'local':
        if len(command_hd_splited) == 4:
            server = verify_source(command_hd_splited[3])
            if not server:
                send_msg(channel_hd,
                         "`El servidor \"{}\" no está en mi inventario de equipos`".format(command_hd_splited[3]))
                return
            else:
                ansible_cmd("win-user-expire-pass-local-msg-slack.yml", channel_hd, user=user, server=server)
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, falta usuario o servidor`")
            return
    elif str(command_hd_splited[1]).lower() == 'ad':
        if len(command_hd_splited) == 3:
            ansible_cmd("win-user-expire-pass-ad-msg-slack.yml", channel_hd, user=user)
        else:
            send_msg(channel_hd, "`Sintaxis incorrecta, hay datos que sobran`")
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"ad\" usuario`")
        return


def win_usuario_borrar(command_hd, channel_hd):
    command_hd_splited = command_hd.split()
    print(command_hd_splited)
    user = command_hd_splited[2]
    server = ""
    if len(command_hd_splited) == 4:
        server = verify_source(command_hd_splited[3])
        if not server:
            send_msg(channel_hd,
                     "`El servidor \"{}\" no está en mi inventario de equipos`".format(command_hd_splited[3]))
            return

    if str(command_hd_splited[1]).lower() == "local" and len(command_hd_splited) == 3:
        send_msg(channel_hd, "`Sintaxis incorrecta, falta el servidor al final del comando`")
    elif str(command_hd_splited[1]).lower() == "local":
        playbook = "win-user-delete-local-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, user=user, server=server)
    elif str(command_hd_splited[1]).lower() == "ad":
        playbook = "win-user-delete-ad-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, user=user)
    else:
        send_msg(channel_hd, "`Sintaxis incorrecta, las opciones son \"local\" o \"ad\" usuario`")
        return


def win_usuario_crear(command_hd, channel_hd):
    # error     @Bot-AD win-usuario-crear ad _nombre_
    # ok        @Bot-AD win-usuario-crear ad _nombre_ _apellido_
    # ok        @Bot-AD win-usuario-crear ad _nombre_ _apellido blabla
    # error     @Bot-AD win-usuario-crear ad _nombre_ _apellido blabla blabla

    # error     @Bot-AD win-usuario-crear local _nombre_
    # error     @Bot-AD win-usuario-crear local _nombre_ _apellido
    # error     @Bot-AD win-usuario-crear local _nombre_ _apellido servernoexite
    # ok        @Bot-AD win-usuario-crear local _nombre_ _apellido win2019srv
    # error     @Bot-AD win-usuario-crear local _nombre_ _apellido blabla servernoexite
    # ok        @Bot-AD win-usuario-crear local _nombre_ _apellido blabla win2019srv
    # error     @Bot-AD win-usuario-crear local _nombre_ _apellido blabla blabla win2019srv

    command_hd_splited = command_hd.split()
    print(command_hd_splited)

    if (len(command_hd_splited) == 4) and (command_hd_splited[1] == 'ad'):
        first_name = command_hd_splited[2]
        last_name = command_hd_splited[3]
        userid = first_name[0] + last_name
        playbook = "win-user-create-ad-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, first_name=first_name, last_name=last_name, userid=userid)

    elif (len(command_hd_splited) == 5) and (command_hd_splited[1] == 'ad'):
        first_name = command_hd_splited[2]
        last_name = command_hd_splited[3]
        extras = command_hd_splited[4]
        userid = first_name[0] + last_name + extras
        playbook = "win-user-create-ad-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, first_name=first_name, last_name=last_name, userid=userid)

    elif (len(command_hd_splited) == 5) and (command_hd_splited[1] == 'local'):
        first_name = command_hd_splited[2]
        last_name = command_hd_splited[3]
        userid = first_name[0] + last_name
        fullname = "\'" + first_name + " " + last_name + "\'"
        server = verify_source(command_hd_splited[4])
        if not server:
            send_msg(channel_hd,
                     "`El servidor \"{}\" no está en mi inventario de equipos`".format(command_hd_splited[4]))
            return
        playbook = "win-user-create-local-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, fullname=fullname, server=server, userid=userid)

    elif (len(command_hd_splited) == 6) and (command_hd_splited[1] == 'local'):
        first_name = command_hd_splited[2]
        last_name = command_hd_splited[3]
        extras = command_hd_splited[4]
        fullname = "\'" + first_name + " " + last_name + extras + "\'"
        userid = first_name[0] + last_name + extras
        server = verify_source(command_hd_splited[5])
        if not server:
            send_msg(channel_hd,
                     "`El servidor \"{}\" no está en mi inventario de equipos`".format(command_hd_splited[5]))
            return
        playbook = "win-user-create-local-msg-slack.yml"
        ansible_cmd(playbook, channel_hd, fullname=fullname, server=server, userid=userid)

    else:
        send_msg(channel_hd, "`Sintaxis incorrecta`")
        return


def authorized_user(slack_userid):
    file = open(_AUTHORIZATION_FILE, 'r')
    authorized_user_ids = file.read()
    file.close()
    if slack_userid in authorized_user_ids:
        return True
    else:
        return False


def handle_command(command_hd, channel_hd):
    """
        Executes bot command if the command is known
    """

    slacklogging.log_msg(bot_log_file, __file__, "Chat Command: " + command_hd + " - On Channel: " + channel_hd)

    if command_hd.startswith("help"):
        response = "```Esta es la lista de commandos que puedes ejecutar:\n" \
                   "- @Bot-AD win-ver-usuario-basico local/AD _user_id_ (opcional _server_)\n" \
                   "- @Bot-AD win-ver-usuario-full local/AD _user_id_ (opcional _server_)\n" \
                   "- @Bot-AD win-desbloquear-usuario local/AD _id_de_usuario_ (opcional _server_)\n" \
                   "- @Bot-AD win-deshabilitar-usuario local/AD _id_de_usuario_ (opcional _server_)\n" \
                   "- @Bot-AD win-usuario-grupo agregar/quitar local/AD _id_de_usuario_ _grupo_ (opcional _server_)\n" \
                   "- @Bot-AD win-usuario-cambiar-password local/ad userid (opcional _server_)\n" \
                   "- @Bot-AD win-usuario-borrar local/ad _id_de_usuario_ (opcional _server_)\n" \
                   "- @Bot-AD win-usuario-crear local/ad _nombre_ _apellido (caracteres opcionales)```"
        send_msg(channel_hd, response)

    elif command_hd.startswith("win-ver-usuario-basico"):
        win_ver_usuario_basico(command_hd, channel_hd)

    elif command_hd.startswith("win-ver-usuario-full"):
        win_ver_usuario_full(command_hd, channel_hd)

    elif command_hd.startswith("win-desbloquear-usuario"):
        win_desbloquear_usuario(command_hd, channel_hd)

    elif command_hd.startswith("win-deshabilitar-usuario"):
        win_deshabilitar_usuario(command_hd, channel_hd)

    elif command_hd.startswith("win-usuario-grupo"):
        win_usuario_grupo(command_hd, channel_hd)

    elif command_hd.startswith("win-usuario-cambiar-password"):
        win_usuario_cambiar_password(command_hd, channel_hd)

    elif command_hd.startswith("win-usuario-borrar"):
        win_usuario_borrar(command_hd, channel_hd)

    elif command_hd.startswith("win-usuario-crear"):
        win_usuario_crear(command_hd, channel_hd)

    else:
        response = "`No conozco ese comando. Intenta con *\"@Bot-AD help\"* para ver la lista de comandos.`"
        send_msg(channel_hd, response)


if __name__ == "__main__":

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read((_NETOR_HOME_DIRECTORY + "netor/netor.config"))
    bot_log_file = config['Slack']['bot_ad_log_file']

    sys.stdout = open(bot_log_file, 'a+')

    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            try:
                command, channel, userid = parse_bot_commands(slack_client.rtm_read())
            except Exception:
                slacklogging.log_msg(bot_log_file, __file__, "Cannot send message to Slack.")
                slacklogging.log_msg(bot_log_file, __file__, Exception)
            else:
                if command:
                    print("UserID= " + userid)
                    print("Command= " + str(command))
                    print("Channel= " + str(channel))
                    if authorized_user(userid):
                        print("Comando Autorizado")
                        handle_command(command, channel)
                    else:
                        print("Comando Denegado")
                        send_msg(channel, "`Usuario \"{}\" no autorizado a ejecutar el comando`".format(userid))

            time.sleep(_RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
