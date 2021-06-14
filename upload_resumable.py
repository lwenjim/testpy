#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os.path
import requests
import hashlib
import json

FILE_UPLOAD = "/Users/jim/Workdata/testphp/src/Nginx/Python.py"
UPLOAD_URL = "http://localhost/upload"
SEGMENT_SIZE = 10


def upload(fp, file_pos, size, file_size):
    session_id = get_session_id()
    fp.seek(file_pos)
    payload = fp.read(size)
    content_range = "bytes {file_pos}-{pos_end}/{file_size}".format(file_pos=file_pos, pos_end=file_pos + size - 1, file_size=file_size)
    headers = {'Content-Disposition': 'attachment; filename="Python.py"', 'Content-Type': 'application/octet-stream', 'X-Content-Range': content_range, 'Session-ID': session_id, 'Content-Length': str(size)}
    res = requests.post(UPLOAD_URL, data=payload, headers=headers)
    if res.text[0:1] != '0':
        print(json.loads(res.text).get('msg'))


def get_session_id():
    m = hashlib.md5()
    file_name = os.path.basename(FILE_UPLOAD)
    m.update(b'123456')
    return m.hexdigest()


def main():
    file_pos = 0
    file_size = os.path.getsize(FILE_UPLOAD)
    fp = open(FILE_UPLOAD, "r")

    while True:
        if file_pos + SEGMENT_SIZE >= file_size:
            upload(fp, file_pos, file_size - file_pos, file_size)
            fp.close()
            break
        else:
            upload(fp, file_pos, SEGMENT_SIZE, file_size)
            file_pos = file_pos + SEGMENT_SIZE


if __name__ == "__main__":
    main()
