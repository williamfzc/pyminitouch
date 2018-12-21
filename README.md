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

with safe_device(_DEVICE_ID) as device:
    device.tap(800, 900)
    device.tap(600, 900)
    device.tap(400, 900)
```

## Installation

Please use python3.

```
pip install pyminitouch
```

### API

Read [demo.py](demo.py) for detail.

## Bug & Suggestion

Please let me know with issue :)

## License

[MIT](LICENSE)
