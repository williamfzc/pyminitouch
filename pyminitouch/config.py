import platform
import subprocess


# connection
DEFAULT_HOST = '127.0.0.1'
PORT_SET = set(range(20000, 21000))
DEFAULT_BUFFER_SIZE = 0
DEFAULT_CHARSET = 'utf-8'

# operation
DEFAULT_DELAY = 0.05

# installer
MNT_PREBUILT_URL = r'https://github.com/williamfzc/stf-binaries/raw/master/node_modules/minitouch-prebuilt/prebuilt'
MNT_HOME = '/data/local/tmp/minitouch'

# system
# 'Linux', 'Windows' or 'Darwin'.
SYSTEM_NAME = platform.system()
NEED_SHELL = SYSTEM_NAME != 'Windows'
ADB_EXECUTOR = 'adb'
