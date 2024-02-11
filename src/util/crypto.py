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
@File       : crypto.py

@Author     : hsn

@Date       : 5/17/23 7:22 PM

@Version    : 1.0.1
"""

import hashlib

import io

from os import PathLike
from pathlib import Path
from typing import IO, Generator, Any


def read_file_chunks(
        file: str | Path | PathLike | IO[bytes], chunk_size: int = io.DEFAULT_BUFFER_SIZE
) -> Generator[bytes, Any, None]:
    """
    Reads a file in chunks of specified size.

    :param file: The file to be read.
    :param chunk_size: The size of the chunks to be read.
    :return: A generator that yields the file contents in chunks.
    """
    if isinstance(file, (str, PathLike)):
        f = open(file, "rb")
    else:
        f = file

    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk


def file_hash(file: str | PathLike | IO[bytes], hasher=None) -> str:
    """
    Computes the hash of a file.
    :param file: The file to be hashed.
    :param hasher: The hasher to use. Defaults to SHA1.
    :return: the hash of the file as a hexadecimal string.
    """
    h = hasher() if hasher is not None else hashlib.sha1(usedforsecurity=False)
    for chunk in read_file_chunks(file):
        h.update(chunk)
    return h.hexdigest()
