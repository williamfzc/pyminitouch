import requests
import tempfile

from pyminitouch import config


def str2byte(content):
    return content.encode(config.DEFAULT_CHARSET)


def download_file(target_url):
    resp = requests.get(target_url)
    with tempfile.NamedTemporaryFile('wb+', delete=False) as f:
        file_name = f.name
        f.write(resp.content)
    return file_name

