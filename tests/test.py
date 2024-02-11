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
@File       : test.py

@Author     : hsn

@Date       : 2/9/24 2:55 PM
"""
import requests
url="http://127.0.0.1:8000/upload"
#url = 'https://telegra.ph/upload'
resp=requests.post(url, files={"file": open("/home/hsn/图片/Transgender_Pride_flag.svg.png", "rb")})
print(resp.text)
# {'src': '/pic/0c52ed8c12b04861a02f1a834b1e3a0d128234901b50b42e0e8a235693e99330'}
#{"src":"/pic/79989891c2b29300fdd2344072f80f25543ad6d6"}
#[{"src":"\/file\/63b519b4de88d9ce6e30c.png"}]
