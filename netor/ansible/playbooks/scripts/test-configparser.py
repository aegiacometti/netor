import configparser
import os

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
_NETOR_HOME_DIRECTORY = os.getenv('NETOR')
netor_config_path_name = _NETOR_HOME_DIRECTORY + "netor/netor.config"
config.read(netor_config_path_name)

print(config['Slack']['bot_win_webhook'])
