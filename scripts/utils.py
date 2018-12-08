import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('/app/config/project.ini')
    return config
