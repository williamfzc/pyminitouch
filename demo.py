import time

from pyminitouch import safe_connection, safe_device, MNTDevice

_DEVICE_ID = '3d33076e'
device = MNTDevice(_DEVICE_ID)

# It's also very important to note that the maximum X and Y coordinates may, but usually do not, match the display size.
# so you need to calculate position by yourself, and you can get maximum X and Y by this way:
print('max x: ', device.connection.max_x)
print('max y: ', device.connection.max_y)

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
device.swipe([(100, 100), (500, 500)])
# of course, with duration and pressure
device.swipe([(100, 100), (400, 400), (200, 400)], duration=500, pressure=59)

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
