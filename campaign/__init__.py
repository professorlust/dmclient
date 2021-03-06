# campaign/__init__.py
# Copyright (C) 2018 Alex Mair. All rights reserved.
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

from datetime import datetime

from sqlalchemy import Column, Integer

from model import CampaignBase, AssetMixin


class Player(CampaignBase, AssetMixin):
    __tablename__ = "players"

    kills = Column(Integer)


class Campaign:
    """
    Because campaigns consist of data that extent far beyond the database,
    ``Campaign``s are not implemented using SQL, instead as plain-old Python
    instances.
    """
    def __init__(self, id, game_system):
        self.id = id
        self.game_system = game_system
        self.name = "Untitled campaign"
        self.author = "Unknown"
        self.description = ""
        self.dice = game_system.dice
        self.creation_date = datetime.now()
        self.revision_date = datetime.now()
        self.players = {}
        self.sessions = []
        self.documents = []
        self.encounters = []
        self.regional_maps = {}
        self.encounter_maps = {}
        self.notes = []


class CampaignSession:
    def __init__(self, timestamp=None, log=""):
        if timestamp is None:
            timestamp = datetime.now()
        self.start_time = timestamp
        self.end_time = timestamp
        self.log = log
        self.attendees = set()
        self.notes = {}
        self.recording = None

    def __str__(self):
        return str(self.start_time)

