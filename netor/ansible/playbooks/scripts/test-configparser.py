import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
netor_config_path_name = "../../../netor.config"
config.read(netor_config_path_name)

print(config['Slack']['bot_win_webhook'])
