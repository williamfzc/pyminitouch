import subprocess
import socket
import time
import os
import random
from contextlib import contextmanager

from pyminitouch.logger import logger
from pyminitouch import config
from pyminitouch.utils import str2byte, download_file, is_port_using, is_device_connected

_ADB = config.ADB_EXECUTOR


class MNTInstaller(object):
    """ install minitouch for android devices """

    def __init__(self, device_id):
        self.device_id = device_id
        self.abi = self.get_abi()
        if self.is_mnt_existed():
            logger.info('minitouch already existed in {}'.format(device_id))
        else:
            self.download_target_mnt()

    def get_abi(self):
        abi = subprocess.getoutput('{} -s {} shell getprop ro.product.cpu.abi'.format(_ADB, self.device_id))
        logger.info('device {} is {}'.format(self.device_id, abi))
        return abi

    def download_target_mnt(self):
        abi = self.get_abi()
        target_url = '{}/{}/bin/minitouch'.format(config.MNT_PREBUILT_URL, abi)
        logger.info('target minitouch url: ' + target_url)
        mnt_path = download_file(target_url)

        # push and grant
        subprocess.check_call([_ADB, '-s', self.device_id, 'push', mnt_path, config.MNT_HOME])
        subprocess.check_call([_ADB, '-s', self.device_id, 'shell', 'chmod', '777', config.MNT_HOME])
        logger.info('minitouch already installed in {}'.format(config.MNT_HOME))

        # remove temp
        os.remove(mnt_path)

    def is_mnt_existed(self):
        file_list = subprocess.check_output([_ADB, '-s', self.device_id, 'shell', 'ls', '/data/local/tmp'])
        return 'minitouch' in file_list.decode(config.DEFAULT_CHARSET)


class MNTServer(object):
    """
    manage connection to minitouch.
    before connection, you should execute minitouch with adb shell.

    command eg::

        adb forward tcp:{some_port} localabstract:minitouch
        adb shell /data/local/tmp/minitouch

    you would better use it via safe_connection ::

        _DEVICE_ID = '123456F'

        with safe_connection(_DEVICE_ID) as conn:
            conn.send('d 0 500 500 50\nc\nd 1 500 600 50\nw 5000\nc\nu 0\nu 1\nc\n')
    """
    _PORT_SET = config.PORT_SET

    def __init__(self, device_id):
        assert is_device_connected(device_id)

        self.device_id = device_id
        logger.info('searching a usable port ...')
        self.port = self._get_port()
        logger.info('device {} bind to port {}'.format(device_id, self.port))

        # check minitouch
        self.installer = MNTInstaller(device_id)

        # keep minitouch alive
        self._forward_port()
        self.mnt_process = None
        self._start_mnt()

        # make sure it's up
        time.sleep(1)
        assert self.heartbeat(), 'minitouch did not work. Try to install it by yourself?'

    def stop(self):
        self.mnt_process and self.mnt_process.kill()
        self._PORT_SET.add(self.port)
        logger.info('device {} unbind to {}'.format(self.device_id, self.port))

    @classmethod
    def _get_port(cls):
        """ get a random port from port set """
        new_port = random.choice(list(cls._PORT_SET))
        if is_port_using(new_port):
            return cls._get_port()
        return new_port

    def _forward_port(self):
        """ allow pc access minitouch with port """
        command_list = [
            _ADB, '-s', self.device_id, 'forward',
            'tcp:{}'.format(self.port),
            'localabstract:minitouch'
        ]
        logger.info('forward command: {}'.format(' '.join(command_list)))
        assert not subprocess.check_output(command_list)

    def _start_mnt(self):
        """ fork a process to start minitouch on android """
        command_list = [
            _ADB, '-s', self.device_id, 'shell',
            '/data/local/tmp/minitouch'
        ]
        logger.info('start minitouch: {}'.format(' '.join(command_list)))
        self.mnt_process = subprocess.Popen(command_list, stdout=subprocess.DEVNULL)

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

        # get minitouch server info
        socket_out = client.makefile()

        # v <version>
        # protocol version, usually it is 1. needn't use this
        socket_out.readline()

        # ^ <max-contacts> <max-x> <max-y> <max-pressure>
        _, max_contacts, max_x, max_y, max_pressure, *_ = \
            socket_out.readline().replace('\n', '').replace('\r', '').split(' ')
        self.max_contacts = max_contacts
        self.max_x = max_x
        self.max_y = max_y
        self.max_pressure = max_pressure

        # $ <pid>
        _, pid = socket_out.readline().replace('\n', '').replace('\r', '').split(' ')
        self.pid = pid

        logger.info('minitouch running on port: {}, pid: {}'.format(self.port, self.pid))
        logger.info('max_contact: {}; max_x: {}; max_y: {}; max_pressure: {}'.format(
            max_contacts, max_x, max_y, max_pressure))

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
def safe_connection(device_id):
    """ safe connection runtime to use """
    # prepare for connection
    server = MNTServer(device_id)
    # real connection
    connection = MNTConnection(server.port)

    yield connection

    # disconnect
    connection.disconnect()
    server.stop()


if __name__ == '__main__':
    _DEVICE_ID = '3d33076e'

    with safe_connection(_DEVICE_ID) as conn:
        # conn.send('d 0 150 150 50\nc\nu 0\nc\n')
        conn.send('d 0 500 500 50\nc\nd 1 500 600 50\nw 5000\nc\nu 0\nu 1\nc\n')
