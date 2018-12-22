import functools
import time
from contextlib import contextmanager

from pyminitouch.logger import logger
from pyminitouch.connection import MNTConnection, MNTServer
from pyminitouch import config
from pyminitouch.utils import restart_adb


def connection_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        operation = func(self, *args, **kwargs)
        logger.info('send operation: {}'.format(operation.replace('\n', '\linesep')))
        time.sleep(config.DEFAULT_DELAY)
        self.connection.send(operation)
    return wrapper


class CommandBuilder(object):
    def __init__(self):
        self._content = ''

    def append(self, new_content):
        self._content += new_content + '\n'

    def commit(self):
        self.append('c')

    def wait(self, ms):
        self.append('w {}'.format(ms))

    def release(self, contact_id):
        self.append('u {}'.format(contact_id))

    def publish(self, connection):
        self.commit()
        final_content = self._content
        logger.info('send operation: {}'.format(final_content.replace('\n', '\\n')))
        time.sleep(config.DEFAULT_DELAY)
        connection.send(final_content)
        self.reset()

    def reset(self):
        self._content = ''


class MNTDevice(object):
    def __init__(self, device_id):
        self.device_id = device_id

        # prepare for connection
        server = MNTServer(device_id)
        # real connection
        connection = MNTConnection(server.port)

        self.server = server
        self.connection = connection

    def stop(self):
        self.connection.disconnect()
        self.server.stop()

    def tap(self, points, pressure=100, duration=None):
        """
        tap on screen, with pressure/duration

        :param points: list, looks like [(x1, y1), (x2, y2)]
        :param pressure: default == 100
        :param duration:
        :return:
        """
        builder = CommandBuilder()
        for point_id, each_point in enumerate(points):
            x, y = each_point
            builder.append('d {} {} {} {}'.format(point_id, x, y, pressure))
        builder.commit()
        # apply duration
        if duration:
            builder.wait(duration)
            builder.commit()
        # release
        for each_id in range(len(points)):
            builder.release(each_id)
        builder.publish(self.connection)
    
    @connection_wrapper
    def swipe(self, points, pressure=100):
        """ swipe from (x1, y1) to (x2, y2) """
        # TODO


@contextmanager
def safe_device(device_id):
    device = MNTDevice(device_id)
    yield device
    device.stop()


if __name__ == '__main__':
    restart_adb()

    _DEVICE_ID = '3d33076e'

    # option1:
    device = MNTDevice(_DEVICE_ID)
    device.tap([(400, 500), (500, 500)], duration=1000)
    time.sleep(1)
    device.stop()

    # option2:
    with safe_device(_DEVICE_ID) as device:
        device.tap([(400, 500), (500, 500)])
        device.tap([(400, 500), (500, 500)])
