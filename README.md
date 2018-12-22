# pyminitouch

[![PyPI version](https://badge.fury.io/py/pyminitouch.svg)](https://badge.fury.io/py/pyminitouch)

python wrapper of [minitouch](https://github.com/openstf/minitouch), for better experience.

[中文文档](README_zh.md)

## TL;DR

An easy way to use [minitouch](https://github.com/openstf/minitouch) with python. 

### Before

- Check device abi
- Download a specified version minitouch
- Install and run it
- Build a socket
- Send message with socket, and your message seems like:
    - `d 0 150 150 50\nc\nu 0\nc\n`
    - hard to read

An unfriendly process.

### After

```python
from pyminitouch.actions import safe_device


_DEVICE_ID = '123456F'
device = MNTDevice(_DEVICE_ID)

# single-tap
device.tap([(400, 600)])
# multi-tap
device.tap([(400, 400), (600, 600)])
# set the pressure, default == 100
device.tap([(400, 600)], pressure=50)

# ... and something else you want, just like minitouch itself!
```

Read [demo.py](demo.py) for detail.

## Installation

Please use python3.

```
pip install pyminitouch
```

## Bug & Suggestion

Please let me know with issue :)

## License

[MIT](LICENSE)
