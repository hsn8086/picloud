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
@File       : main.py

@Author     : hsn

@Date       : 2/9/24 2:30 PM
"""
import sqlite3
import tempfile
from pathlib import Path

import PIL
import fastapi
import uvicorn
from PIL import Image
from fastapi import FastAPI, UploadFile

from src.util.file import FileData
from src.util.network import TelegraPh

app = FastAPI()
Path("data").mkdir(exist_ok=True)
db = sqlite3.connect(Path("data/data.sqlite").as_posix())
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS telegraph (hash TEXT PRIMARY KEY, path TEXT)')
if (path := Path("data/pic_cache.json")).exists():
    fd = FileData.load(path)
else:
    fd = FileData(Path("data/pic_cache"), max_size=5 * 1024 * 1024 * 1024)
proxy = "http://127.0.0.1:7890"
tg = TelegraPh(_proxy=proxy)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
@app.put("/upload")
async def upload(file: UploadFile):
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    pic_cache_folder = data_folder / "pic_cache"
    pic_cache_folder.mkdir(exist_ok=True)

    with tempfile.TemporaryFile('wb+') as temp:
        while chunk := await file.read(1024):
            temp.write(chunk)
        try:
            temp.seek(0)
            Image.open(temp).verify()
        except PIL.UnidentifiedImageError:
            return {"status": "error", "message": "not a pic"}
        temp.seek(0)
        uid = await tg.upload(temp.read())

        temp.seek(0)
        _hash = fd.add_file(temp)
        db.execute("INSERT INTO telegraph (hash, path) VALUES (?, ?)", (_hash, uid))
    return {"src": f"/pic/{_hash}"}


@app.get("/pic/{pic_hash}")
async def get_pic(pic_hash: str):
    pic_hash = pic_hash.split(".")[0]
    if fd.exist(pic_hash):
        data_folder = Path("data")
        pic_cache_folder = data_folder / "pic_cache"
        rt_data = (pic_cache_folder / pic_hash).open('rb')
        fd.renew_file(pic_hash)
    else:
        if (r := cursor.execute("SELECT path FROM telegraph WHERE hash=?", (pic_hash,)).fetchone()) is not None:
            try:
                rt_data = await tg.get_stream(r[0])
            except Exception as e:
                return fastapi.Response(content=str(e), status_code=500)
        else:
            return fastapi.Response(content="not found", status_code=404)

    rt_data.seek(0)
    img = Image.open(rt_data)
    rt_data.seek(0)
    resp = fastapi.responses.Response(content=rt_data.read(), media_type=f"image/{img.format.lower()}")

    return resp


config = uvicorn.Config(
    app,
    host="0.0.0.0",
    port=8000,
    log_level="info",
    reload=False,
    workers=16,
    loop="asyncio",
)
# print(asyncio.run(tg.upload(open("/home/hsn/图片/Transgender_Pride_flag.svg.png", "rb"))))
# print(asyncio.run(tg.get('/file/74fcd5df548f399e4e1gg.png')))
s = uvicorn.Server(config)
s.run()
fd.dump(Path("data/pic_cache.json"))
db.commit()
db.close()
