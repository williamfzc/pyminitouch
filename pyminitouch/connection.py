import subprocess
import socket
import time
from contextlib import contextmanager

from pyminitouch.logger import logger
from pyminitouch import config
from pyminitouch.utils import str2byte


class MNTInstaller(object):
    """ install minitouch for android devices """
    # TODO match version
    # TODO auto install


class MNTServer(object):
    """
    before connection, you should execute minitouch with adb shell.

    command eg:
        adb forward tcp:{some_port} localabstract:minitouch
        adb shell /data/local/tmp/minitouch
    """
    _PORT_SET = config.PORT_SET

    def __init__(self, device_id):
        self.device_id = device_id
        self.port = self._get_port()
        logger.info('device {} bind to port {}'.format(device_id, self.port))

        # keep minitouch alive
        self._forward_port()
        self.mnt_process = None
        self._start_mnt()

        # make sure it's up
        time.sleep(1)
        assert self.heartbeat()

    def __del__(self):
        self.mnt_process and self.mnt_process.kill()
        self._PORT_SET.add(self.port)
        logger.info('device {} unbind to {}'.format(self.device_id, self.port))

    @classmethod
    def _get_port(cls):
        """ get a random port from port set """
        # TODO should check if this port has been used
        return cls._PORT_SET.pop()

    def _forward_port(self):
        """ allow pc access minitouch with port """
        command_list = [
            'adb', '-s', self.device_id, 'forward',
            'tcp:{}'.format(self.port),
            'localabstract:minitouch'
        ]
        logger.info('forward command: {}'.format(' '.join(command_list)))
        assert not subprocess.check_output(command_list)

    def _start_mnt(self):
        """ fork a process to start minitouch on android """
        command_list = [
            'adb', '-s', self.device_id, 'shell',
            '/data/local/tmp/minitouch'
        ]
        logger.info('start minitouch: {}'.format(' '.join(command_list)))
        self.mnt_process = subprocess.Popen(command_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def heartbeat(self):
        """ check if minitouch process alive """
        return self.mnt_process.poll() is None


class MNTConnection(object):
    """ manage socket connection between pc and android """
    _DEFAULT_HOST = config.DEFAULT_HOST
    _DEFAULT_BUFFER_SIZE = config.DEFAULT_BUFFER_SIZE

    def __init__(self, port):
        self.port = port

        # build connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self._DEFAULT_HOST, self.port))
        self.client = client
        logger.info('minitouch connected on {}'.format(self.port))

    def disconnect(self):
        self.client and self.client.close()
        self.client = None
        logger.info('minitouch disconnected')

    def send(self, content):
        """ send message and get its response """
        byte_content = str2byte(content)
        self.client.sendall(byte_content)
        return self.client.recv(self._DEFAULT_BUFFER_SIZE)


@contextmanager
def build_connection(device_id):
    # prepare for connection
    server = MNTServer(device_id)
    # real connection
    connection = MNTConnection(server.port)

    yield connection

    # disconnect
    connection.disconnect()
    del server


if __name__ == '__main__':
    _DEVICE_ID = '3d33076e'

    with build_connection(_DEVICE_ID) as conn:
        conn.send('d 0 150 150 50\nc\nu 0\nc\n')
