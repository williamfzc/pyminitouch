import time

from pyminitouch.connection import safe_connection
from pyminitouch.actions import MNTDevice, safe_device


_DEVICE_ID = '3d33076e'

# high level API
# option1:
device = MNTDevice(_DEVICE_ID)

device.tap(600, 900)
device.tap(400, 900)

# for long-click, you should control time delay by yourself
# because minitouch return nothing when actions done
# we will never know the time when it finished
device.tap(800, 900, duration=1000)
time.sleep(1)

device.swipe(100, 100, 800, 800)

device.stop()

# option2:
with safe_device(_DEVICE_ID) as device:
    device.tap(800, 900)
    device.tap(600, 900)
    device.tap(400, 900)


# low level API
_OPERATION = '''
d 0 150 150 50\n
c\n
u 0\n
c\n
'''

with safe_connection(_DEVICE_ID) as conn:
    conn.send(_OPERATION)
