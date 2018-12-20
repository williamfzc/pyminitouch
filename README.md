# pyminitouch

**STILL IN PROGRESS**

python wrapper of [minitouch](https://github.com/openstf/minitouch), for better experience.

## 目标

该项目将对 [minitouch](https://github.com/openstf/minitouch) 进行封装，致力于降低使用成本，使这个库能够更好的被利用起来。

## 意义

minitouch 是 openstf 基于 ndk + android 开发的用于模拟人类点击行为的操作库。这个库以高稳定性、反应快著称，比起adb操作与uiautomator都要更灵敏，被广泛用于android设备的精细操作。

然而，因为其使用与安装的方式都较为繁琐，且无法定位到元素，使得它在自动化的应用领域上远远比不上uiautomator。

但他的实现机制与其他模拟方式不同，能够真正模拟物理点击的效果（uiautomator属于软件层面上的模拟），更加接近真实点击的效果。举个例子，打开 开发者模式-显示点击位置，同类产品在模拟点击时不会有"小圆圈"，而minitouch有，表现与真实人手点击一致。

## 设计

### 层级架构

- [x] 连接层
    - 管理与android设备上的minitouch的连接
    - 稳定性与连接机制等
- [x] 基础方法层
    - 将minitouch提供的简单原生方法进行基础封装
    - 基础方法可被用于构建上层应用
- [ ] 自定义方法层
    - 将基础方法进行二次封装达到更复杂的操作效果
    - 方便开发者进行自由定制

### API

#### Normal API

pyminitouch解放了原来非常难用的方法，你可以用下面两种方式进行调用。

```python
from pyminitouch.actions import MNTDevice, safe_device


_DEVICE_ID = '3d33076e'

# option1:
device = MNTDevice(_DEVICE_ID)

device.tap(800, 900, 50)
device.tap(600, 900, 50)
device.tap(400, 900, 50)

device.stop()

# option2:
with safe_device(_DEVICE_ID) as device:
    device.tap(800, 900, 50)
    device.tap(600, 900, 50)
    device.tap(400, 900, 50)

```

#### Low Level API

你可以将pyminitouch作为一个简单的socket通信使用：

```python
from pyminitouch.connection import safe_connection


_DEVICE_ID = '3d33076e'
_OPERATION = '''
d 0 150 150 50\n
c\n
u 0\n
c\n
'''

with safe_connection(_DEVICE_ID) as conn:
    conn.send(_OPERATION)
```

## TODO

- [ ] 根据手机类型自动安装指定版本的 minitouch
- [ ] 端口占用检查

## Bug & 建议

请直接提issue

## 协议

[MIT](LICENSE)
