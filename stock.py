__author__ = 'yu'

import requests

url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=sh000001'

r = requests.get(url, headers={
    "apikey": "b6c534ca395655349ec1ae49e774a3e1"
})

print r.json()['retData']['stockinfo']['currentPrice']