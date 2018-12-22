import requests
import tempfile
import socket
import subprocess

from pyminitouch import config


def str2byte(content):
    """ compile str to byte """
    return content.encode(config.DEFAULT_CHARSET)


def download_file(target_url):
    """ download file to temp path, and return its file path for further usage """
    resp = requests.get(target_url)
    with tempfile.NamedTemporaryFile('wb+', delete=False) as f:
        file_name = f.name
        f.write(resp.content)
    return file_name


def is_port_using(port_num):
    """ if port is using by others, return True. else return False """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    status = False
    try:
        s.connect((config.DEFAULT_HOST, int(port_num)))
        s.shutdown(2)
    except ConnectionRefusedError:
        status = True
    finally:
        return status


def restart_adb():
    """ restart adb server """
    _ADB = config.ADB_EXECUTOR
    subprocess.check_call([_ADB, 'kill-server'])
    subprocess.check_call([_ADB, 'start-server'])
