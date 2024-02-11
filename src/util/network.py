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
@File       : network.py

@Author     : hsn

@Date       : 2/10/24 9:33 PM
"""
import json
import tempfile
from typing import IO

import aiohttp


class TelegraPh:
    def __init__(self, _proxy: str | None = None):
        self._proxy = _proxy

    async def upload(self, file: bytes | IO) -> str:
        url = 'https://telegra.ph/upload'
        files = {'file': file}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=files, proxy=self._proxy) as r:

                resp: dict | list = json.loads(await r.text())
                if isinstance(resp, dict):
                    if resp.get("error", None) is not None:
                        raise Exception(f"error: {resp['error']}")
                return resp[0]['src']

    async def get(self, path: str):
        url = f"https://telegra.ph/{path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=self._proxy) as r:
                if r.status != 200:
                    raise Exception(f"status code is {r.status}")
                return await r.read()

    async def get_stream(self, path: str):
        url = f"https://telegra.ph/{path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=self._proxy) as r:
                if r.status != 200:
                    raise Exception(f"status code is {r.status}")
                temp = tempfile.TemporaryFile("wb+")
                while chunk := await r.content.read(1024):
                    temp.write(chunk)

                return temp
