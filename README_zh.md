# pyminitouch

[![PyPI version](https://badge.fury.io/py/pyminitouch.svg)](https://badge.fury.io/py/pyminitouch)

python wrapper of [minitouch](https://github.com/openstf/minitouch), for better experience.

[English Document](README.md)

## 目标

该项目将对 [minitouch](https://github.com/openstf/minitouch) 进行封装，致力于降低使用成本，使这个库能够更好的被利用起来。

## TL;DR

### 以前

- 检查设备CPU类型
- 下载指定版本的minitouch（或者自己build）
- 把它push到手机上，授权，运行它
- 创建socket，连接到它
- 通过socket传递信息，然而你的信息看起来是这样的：
    - `d 0 150 150 50\nc\nu 0\nc\n`
    - 可读性较低

是个非常繁琐的流程。

### 现在

```python
from pyminitouch import MNTDevice


_DEVICE_ID = '123456F'
device = MNTDevice(_DEVICE_ID)

# single-tap
device.tap([(400, 600)])
# multi-tap
device.tap([(400, 400), (600, 600)])
# set the pressure, default == 100
device.tap([(400, 600)], pressure=50)

# 可以直接用简洁的API调用minitouch提供的强大功能！
```

你不再需要关心依赖安装、设备版本之类的事情。直接跑脚本就行了！

更多使用方式见 [demo.py](demo.py)

## 安装

请使用python3

```
pip install pyminitouch
```

## 实现原理

其实跟TLDR提到的"以前的"流程是一样的。

## 意义

minitouch 是 openstf 基于 ndk + android 开发的用于模拟人类点击行为的操作库。这个库以高稳定性、反应快著称，比起adb操作与uiautomator都要更灵敏，被广泛用于android设备的精细操作。

然而，因为其使用与安装的方式都较为繁琐，且无法定位到元素，使得它在自动化的应用领域上远远比不上uiautomator。

但他的实现机制与其他模拟方式不同，能够真正模拟物理点击的效果（uiautomator属于软件层面上的模拟），更加接近真实点击的效果。举个例子，打开 开发者模式-显示点击位置，同类产品在模拟点击时不会有"小圆圈"，而minitouch有，表现与真实人手点击一致。

## Bug & 建议

请直接提issue

## 协议

[MIT](LICENSE)
