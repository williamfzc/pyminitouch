import time

from pyminitouch.connection import safe_connection
from pyminitouch.actions import MNTDevice, safe_device


_DEVICE_ID = '4df189487c7b6fef'
device = MNTDevice(_DEVICE_ID)

# single-tap
device.tap([(400, 600)])
# multi-tap
device.tap([(400, 400), (600, 600)])
# set the pressure, default == 100
device.tap([(400, 600)], pressure=50)

# long-time-tap
# for long-click, you should control time delay by yourself
# because minitouch return nothing when actions done
# we will never know the time when it finished
device.tap([(400, 600)], duration=1000)
time.sleep(1)


# swipe
device.swipe([(100, 100), (800, 800)])

# stop minitouch
# when it was stopped, minitouch can do nothing for device, including release.
device.stop()


# In another way, you needn't consider about device's life-cycle.
# context manager will handle it
with safe_device(_DEVICE_ID) as device:
    # single-tap
    device.tap([(400, 600)])
    # multi-tap
    device.tap([(400, 400), (600, 600)])
    # set the pressure, default == 100
    device.tap([(400, 600)], pressure=50)


# What's more, you can also access low level API for further usage.
# send raw text to it
_OPERATION = '''
d 0 150 150 50\n
c\n
u 0\n
c\n
'''

with safe_connection(_DEVICE_ID) as conn:
    conn.send(_OPERATION)
