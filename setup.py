# setup.py
# Copyright (C) 2017 Alex Mair. All rights reserved.
# This file is part of dmclient.
#
# dmclient is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# dmclient is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dmclient.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

from core.config import APP_DESCRIPTION, APP_VERSION, APP_NAME

APP = ['dmclient.py']
DATA_FILES = []
OPTIONS = {}

setup(name=APP_NAME, version=APP_VERSION, description=APP_DESCRIPTION,
      app=APP,
      data_files=DATA_FILES,
      options={'py2app': OPTIONS},
      setup_requires=['py2app'],
      )
