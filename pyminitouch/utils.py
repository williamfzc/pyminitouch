from pyminitouch import config


def str2byte(content):
    return content.encode(config.DEFAULT_CHARSET)
