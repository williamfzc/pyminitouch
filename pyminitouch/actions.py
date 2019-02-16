import time
from contextlib import contextmanager

from pyminitouch.logger import logger
from pyminitouch.connection import MNTConnection, MNTServer, safe_connection
from pyminitouch import config
from pyminitouch.utils import restart_adb


class CommandBuilder(object):
    """ build command str for minitouch

    You can use this, to custom actions as you wish.
    eg:
        with safe_connection(_DEVICE_ID) as connection:
            builder = CommandBuilder()
            builder.down(0, 400, 400, 50)
            builder.commit()
            builder.move(0, 500, 500, 50)
            builder.commit()
            builder.move(0, 800, 400, 50)
            builder.commit()
            builder.up(0)
            builder.commit()
            builder.publish(connection)

    use `d.connection` to get `connection` from device
    """

    # TODO (x, y) can not beyond the screen size
    def __init__(self):
        self._content = ''

    def append(self, new_content):
        self._content += new_content + '\n'

    def commit(self):
        """ minitouch command, eg: 'c\n' """
        self.append('c')

    def wait(self, ms):
        """ minitouch command, eg: 'w 1000\n' """
        self.append('w {}'.format(ms))

    def up(self, contact_id):
        """ minitouch command, eg: 'u 0\n' """
        self.append('u {}'.format(contact_id))

    def down(self, contact_id, x, y, pressure):
        """ minitouch command, eg: 'd 0 200 200 50\n' """
        self.append('d {} {} {} {}'.format(contact_id, x, y, pressure))

    def move(self, contact_id, x, y, pressure):
        """ minitouch command, eg: 'm 0 200 200 50\n' """
        self.append('m {} {} {} {}'.format(contact_id, x, y, pressure))

    def publish(self, connection):
        """ apply current command, to your device """
        self.commit()
        final_content = self._content
        logger.info('send operation: {}'.format(final_content.replace('\n', '\\n')))
        time.sleep(config.DEFAULT_DELAY)
        connection.send(final_content)
        self.reset()

    def reset(self):
        """ clear current command """
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
            builder.up(each_id)
        builder.publish(self.connection)

    def swipe(self, points, pressure=100, duration=None):
        """
        swipe between points, one by one

        :param points: [(400, 500), (500, 500)]
        :param pressure: default == 100
        :param duration:
        :return:
        """
        builder = CommandBuilder()
        point_id = 0
        # tap the first point
        x, y = points.pop(0)
        builder.append('d {} {} {} {}'.format(point_id, x, y, pressure))
        builder.commit()
        builder.publish(self.connection)

        # start swiping
        for each_point in points:
            if duration:
                time.sleep(duration / 1000)
            x, y = each_point
            builder.append('m {} {} {} {}'.format(point_id, x, y, pressure))
            builder.commit()
            builder.publish(self.connection)
        # release
        builder.up(point_id)

    # extra functions' name starts with 'ext_'
    def ext_smooth_swipe(self, points, pressure=100, duration=None, part=10):
        """
        smoothly swipe between points, one by one
        it will split distance between points into pieces

        e.g:
            before:
                points == [(100, 100), (500, 500)]
                part == 8
            after:
                points == [(100, 100), (150, 150), (200, 200), ... , (500, 500)]

        :param points:
        :param pressure:
        :param duration:
        :param part: default to 10
        :return:
        """
        for each_index in range(len(points) - 1):
            cur_point = points[each_index]
            next_point = points[each_index + 1]

            offset = (int((next_point[0] - cur_point[0]) / part),
                      int((next_point[1] - cur_point[1]) / part))
            new_points = [(cur_point[0] + i * offset[0], cur_point[1] + i * offset[1]) for i in range(part)]
            new_points.append(points[-1])
            self.swipe(new_points, pressure=pressure, duration=duration)


@contextmanager
def safe_device(device_id):
    device = MNTDevice(device_id)
    yield device
    time.sleep(config.DEFAULT_DELAY)
    device.stop()


if __name__ == '__main__':
    restart_adb()

    _DEVICE_ID = '4df189487c7b6fef'

    with safe_connection(_DEVICE_ID) as d:
        builder = CommandBuilder()
        builder.down(0, 400, 400, 50)
        builder.commit()
        builder.move(0, 500, 500, 50)
        builder.commit()
        builder.move(0, 800, 400, 50)
        builder.commit()
        builder.up(0)
        builder.commit()
        builder.publish(d)

    with safe_device(_DEVICE_ID) as d:
        builder = CommandBuilder()
        builder.down(0, 400, 400, 50)
        builder.commit()
        builder.move(0, 500, 500, 50)
        builder.commit()
        builder.move(0, 800, 400, 50)
        builder.commit()
        builder.up(0)
        builder.commit()
        builder.publish(d.connection)

    # option1:
    device = MNTDevice(_DEVICE_ID)
    device.tap([(400, 500), (500, 500)], duration=1000)

    # you should control time delay by yourself
    # otherwise when connection lost, action will never stop.
    time.sleep(1)

    device.stop()

    # option2:
    with safe_device(_DEVICE_ID) as device:
        device.tap([(400, 500), (500, 500)])
        device.swipe([(400, 500), (500, 500)], duration=500)
        time.sleep(0.5)
