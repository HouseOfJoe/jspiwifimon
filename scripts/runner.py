import os
import re
import subprocess
import time
from datetime import datetime,date
import requests
from json import dumps

response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping[0] = ping[0].replace(',', '.')
download[0] = download[0].replace(',', '.')
upload[0] = upload[0].replace(',', '.')

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
date = '2019-01-02'


sender = {'ping': ping[0],'download': download[0],'upload': upload[0],'date': date}
res = requests.post('http://127.0.0.1:5000/api/vi/entry', json=sender)
print(res.text)
senderserve = res.json
print('{0},{1},{2},{3}'.format(date, ping[0], download[0], upload[0]))



