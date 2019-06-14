from setuptools import setup, find_packages


setup(
    name='pyminitouch',
    version='0.3.0',
    description='python wrapper of minitouch, for better experience',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/pyminitouch',
    packages=find_packages(),
    install_requires=[
        'loguru',
        'requests',
    ]
)
