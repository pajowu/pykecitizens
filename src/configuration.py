import configparser
import os


def load_config(config_file):
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    return config


def save_config(config_file, config):
    with open(config_file, "w") as configfile:
        config.write(configfile)
