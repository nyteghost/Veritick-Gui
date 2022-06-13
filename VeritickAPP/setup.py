from setuptools import find_packages
from distutils.core import setup
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
	# Name of the package 
	name='VeritickAPP',
	# Packages to include into the distribution 
	packages=find_packages('.'),
	# Start with a small number and increase it with 
	# every change you make https://semver.org 
	version='1.0.0',
	# Chose a license from here: https: // 
	# help.github.com / articles / licensing - a - 
	# repository. For example: MIT 
	license='',
	# Short description of your library 
	description='',
	# Long description of your library 
	long_description=long_description,
	long_description_content_type='text/markdown',
	# Your name 
	author='Mark Brown',
	# Your email 
	author_email='mbrown@sca-atl.com',
	# Either the link to your github or to your website 
	url='',
	# Link from which the project can be downloaded 
	download_url='',
	# List of keywords 
	keywords=[],
	# List of packages to install with this one 
	install_requires=['aiohttp-cors==0.7.0', 'aiohttp==3.8.1', 'aiosignal==1.2.0', 'altgraph==0.17.2', 'ansicon==1.89.0', 'appdata==1.2.0', 'appdirs==1.4.4', 'args==0.1.0', 'astor==0.8.1', 'asttokens==2.0.5', 'async-timeout==4.0.2', 'attrs==21.4.0', 'auto-py-to-exe==2.20.1', 'backcall==0.2.0', 'better-exceptions==0.3.3', 'blessed==1.19.1', 'bottle-websocket==0.2.9', 'bottle==0.12.21', 'cachetools==5.1.0', 'certifi==2022.5.18.1', 'cffi==1.15.0', 'charset-normalizer==2.0.12', 'click-default-group==1.2.2', 'click==7.0', 'clint==0.5.1', 'colorama==0.4.4', 'colorful==0.5.4', 'commonmark==0.9.1', 'customtkinter==4.2.0', 'cycler==0.11.0', 'darkdetect==0.6.0', 'decorator==5.1.1', 'distlib==0.3.4', 'eel==0.14.0', 'executing==0.8.3', 'fernet==1.0.1', 'filelock==3.7.0', 'fonttools==4.33.3', 'frozenlist==1.3.0', 'fsspec==2022.5.0', 'future==0.18.2', 'fuzzywuzzy==0.18.0', 'gevent-websocket==0.10.1', 'gevent==21.12.0', 'google-api-core==2.8.0', 'google-auth==2.6.6', 'googleapis-common-protos==1.56.1', 'gpustat==1.0.0b1', 'greenlet==1.1.2', 'grpcio==1.43.0', 'h5py==3.7.0', 'idna==3.3', 'ipython==8.3.0', 'jedi==0.18.1', 'jinxed==1.2.0', 'jsonschema==4.5.1', 'kiwisolver==1.4.2', 'loguru==0.4.1', 'matplotlib-inline==0.1.3', 'matplotlib==3.5.2', 'mouseinfo==0.1.3', 'msgpack==1.0.3', 'multidict==6.0.2', 'numexpr==2.8.1', 'numpy==1.22.4', 'nvidia-ml-py3==7.352.0', 'opencensus-context==0.1.2', 'opencensus==0.9.0', 'packaging==21.3', 'pandas==1.4.2', 'pandastable==0.13.0', 'parso==0.8.3', 'pefile==2022.5.30', 'pickleshare==0.7.5', 'pillow==9.1.1', 'pip==22.1.2', 'platformdirs==2.5.2', 'plotly==5.8.0', 'prometheus-client==0.13.1', 'prompt-toolkit==3.0.29', 'protobuf==3.20.1', 'psutil==5.9.1', 'pure-eval==0.2.2', 'py-spy==0.3.12', 'pyaes==1.6.1', 'pyarrow==8.0.0', 'pyasn1-modules==0.2.8', 'pyasn1==0.4.8', 'pyautogui==0.9.53', 'pycparser==2.21', 'pygetwindow==0.0.9', 'pygments==2.12.0', 'pyinstaller-hooks-contrib==2022.6', 'pyinstaller==5.1', 'pymsgbox==1.0.9', 'pynput==1.7.6', 'pyodbc==4.0.32', 'pyparsing==3.0.9', 'pyperclip==1.8.2', 'pypubsub==4.0.3', 'pyqt5-qt5==5.15.2', 'pyqt5-sip==12.10.1', 'pyqt5==5.15.6', 'pyqtwebengine-qt5==5.15.2', 'pyqtwebengine==5.15.5', 'pyrect==0.2.0', 'pyrsistent==0.18.1', 'pyscreeze==0.1.28', 'python-dateutil==2.8.2', 'python-levenshtein==0.12.2', 'pytweening==1.0.4', 'pytz==2022.1', 'pywin32-ctypes==0.2.0', 'pywin32==304', 'pyyaml==6.0', 'qtstylish==0.1.5', 'redis==3.5.3', 'requests==2.27.1', 'rich==12.4.4', 'rsa==4.8', 'setup-py-cli==2.1.0', 'setuptools==60.6.0', 'six==1.16.0', 'smart-open==6.0.0', 'sqlalchemy==1.4.36', 'stack-data==0.2.0', 'tables==3.7.0', 'tenacity==8.0.1', 'tk==0.1.0', 'traitlets==5.2.1.post0', 'typing-extensions==4.2.0', 'urllib3==1.26.9', 'virtualenv==20.14.1', 'wcwidth==0.2.5', 'wheel==0.37.1', 'whichcraft==0.6.1', 'win32-setctime==1.1.0', 'wordcloud==1.8.1', 'wxpython==4.1.1', 'xlrd==2.0.1', 'xlwings==0.27.8', 'yarl==1.7.2', 'zope.event==4.5.0', 'zope.interface==5.4.0'],
	# https://pypi.org/classifiers/
	classifiers=[]
)
