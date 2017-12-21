# core/archive.py
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

.. note ::
    For whatever reason, ``tarfile`` on Windows uses forward slashes instead
    of ``os.sep``. As a result, this module never makes use of
    ``os.path.join()``.
"""

import tarfile
from json import JSONDecodeError
from logging import getLogger

from sqlalchemy import Column, String

from model import DescribableMixin, Base
from model.schema import *

__all__ = ["InvalidArchiveError", "InvalidSessionError", "ArchiveMeta",
           "InvalidArchiveMetadataError", "open_archive", "open_campaign"]

_open = open

log = getLogger(__name__)  # TODO archives should not require logging.


class InvalidArchiveError(Exception):
    """Raised when an archive is corrupt or missing essential data."""


class NoSuchDirectoryError(InvalidArchiveError):
    pass


class NoSuchArchiveFileError(InvalidArchiveError):
    pass


class InvalidSessionError(InvalidArchiveError):
    """Raised when a campaign archive contains invalid data."""


def open_campaign(path):
    return open_archive(path)


def open_archive(path):
    schema = ArchiveMetaSchema()
    return ArchiveMeta.load(path)


def unpack_archive(meta, destination):
    with tarfile.open(meta.last_seen_path, "r:bz2") as f:
        f.extractall(destination)


class ArchiveMeta:
    def __init__(self, id, game_system_id, name="", description="", author="",
                 creation_date=None, revision_date=None, isbn=None,
                 last_seen_path=None):
        self.id = id
        self.game_system_id = game_system_id
        self.name = name
        self.description = description
        self.author = author
        self.creation_date = creation_date
        self.revision_date = revision_date
        self.isbn = isbn
        self.last_seen_path = last_seen_path

    @classmethod
    def load(cls, path):
        """
        :return: An ``ArchiveMeta`` instance.
        :raises: InvalidArchiveMetadataError
        """
        try:
            with tarfile.open(path, "r:bz2") as tf:
                meta = _parse_json(tf.extractfile("properties.json"),
                                   ArchiveMetaSchema)
                meta.last_seen_path = path
                return meta
        except (tarfile.ReadError, EOFError, JSONDecodeError):
            raise InvalidArchiveMetadataError(
                "invalid archive meta {}".format(path))


class ArchiveMetaSchema(Schema):
    """
    This schema stores the specification for the toplevel ``properties.json``
    found in an archive.
    """

    class Meta:
        ordered = True

    id = fields.UUID(required=True)
    game_system_id = fields.Str(required=True)
    name = fields.Str(default="")
    description = fields.Str(default="")
    author = fields.Str(default="")
    creation_date = fields.DateTime(format="iso")
    revision_date = fields.DateTime(format="iso")
    isbn = fields.Str(default="")

    @post_load
    def make_meta(self, m):
        return ArchiveMeta(**m)


def _parse_json(f, schemacls):
    """
    :param f: file-like object to read json from
    :param schemacls: the schema to parse the properties with
    :return: a dictionary containing the validated object
    :raises: JSONDecodeError if the JSON is malformed
    """
    schema = schemacls()
    try:
        obj, errors = schema.loads(f.read())
        if errors:
            log.debug("validation errors: %s", errors)
            raise JSONDecodeError("schema validation failed", "", 0)
        return obj
    except ValueError:
        raise JSONDecodeError("", "", pos=0)


class InvalidArchiveMetadataError(InvalidArchiveError):
    pass


class ArchiveMetaSql(Base, DescribableMixin):
    __tablename__ = "archives"

    isbn = Column(String)

    def __init__(self, tarfile, path):
        """

        :param tarfile:
        :param path: Because tarfile is wonderful and doesn't keep it.
        """
        self.tarfile = tarfile
        self.path = path
