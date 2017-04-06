import sys
from distutils.core import setup

if sys.version_info < (2, 7):
    print("THIS MODULE REQUIRES PYTHON 2.6, 2.7. YOU ARE CURRENTLY USING PYTHON {0}".format(sys.version))
    sys.exit(1)

setup(
    name='x-copilot',
    version='0.1.0',
    url='https://github.com/owentar/x-copilot/',
    license='MIT',
    author='Hernan Carrizo',
    description='A voice commanded copilot for X-Plane flight simulator',
    platforms='any',
    scripts=['PI_xcopilot.py'],
    packages=['xcopilot', 'xcopilot.config', 'xcopilot.config.aircraft', 'xcopilot.xplane'],
    package_dir={ 'xcopilot': 'xcopilot' }
)
