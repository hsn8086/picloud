#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2023. HCAT-Project-Team
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : file.py

@Author     : hsn

@Date       : 2/10/24 9:32 PM
"""
import json
from collections import deque
from hashlib import sha256
from pathlib import Path
from typing import IO

from src.util.crypto import file_hash


class FileData:
    def __init__(self, folder: Path, max_size: int = 1000 * 1024 * 1024):
        self.fmt_queue = deque()
        self.file_size_dict = {}
        self.max_size = max_size
        self.folder = folder
        self.folder.mkdir(exist_ok=True, parents=True)

    def calc_size(self):
        size = 0
        for i in self.file_size_dict.values():
            size += i
        return size

    def add_file(self, file: IO) -> str:
        file.seek(0)
        _hash = file_hash(file, hasher=sha256)
        file_size = file.seek(0, 2)
        file.seek(0)
        file_path = self.folder / _hash
        while chunk := file.read(4096):
            file_path.write_bytes(chunk)
        self.file_size_dict[_hash] = file_size
        self.fmt_queue.append(_hash)
        self.clear_file()
        return _hash

    def renew_file(self, _hash: str):
        self.fmt_queue.remove(_hash)
        self.fmt_queue.append(_hash)

    def clear_file(self):
        size = self.calc_size()
        over_size = size - self.max_size
        while over_size > 0:
            _hash = self.fmt_queue.popleft()
            file_size = self.file_size_dict[_hash]
            (self.folder / _hash).unlink()
            self.file_size_dict.pop(_hash)
            over_size -= file_size

    def exist(self, _hash: str):
        return _hash in self.file_size_dict

    def dumps(self) -> str:
        j = {"file_size_dict": self.file_size_dict, "fmt_queue": list(self.fmt_queue),
             "folder": self.folder.as_posix(), "max_size": self.max_size}
        return json.dumps(j)

    @staticmethod
    def loads(data: dict | str) -> 'FileData':
        if isinstance(data, str):
            data = json.loads(data)
        fd = FileData(Path(data["folder"]), data["max_size"])
        fd.file_size_dict = data["file_size_dict"]
        fd.fmt_queue = deque()
        fd.fmt_queue.extend(data["fmt_queue"])
        return fd

    def dump(self, path: Path):
        path.write_text(self.dumps())

    @staticmethod
    def load(path: Path):
        data = json.loads(path.read_text())
        return FileData.loads(data)
