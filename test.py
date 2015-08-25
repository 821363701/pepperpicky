__author__ = 'yu'

import requests
from BeautifulSoup import BeautifulSoup, NavigableString
from PIL import Image
from io import BytesIO

def print_beautiful(content):
    for item in content.contents:
        if type(item) == NavigableString:
            continue

        if item.name == 'p':
            print item.text
        elif item.name == 'img':
            for key, value in item.attrs:
                if key == 'src':
                    print value
                    res = requests.get(value)
                    img = Image.open(BytesIO(res.content))
                    img.show()
                    break
        elif item.name == 'div':
            print_beautiful(item)
        else:
            print 'unrecognized tag'



topic_url = u'http://www.douban.com/group/topic/78977827'

r = requests.get(topic_url)
soup = BeautifulSoup(r.text)
r.close()

content = soup.find('div', {'class': 'topic-content'})
print_beautiful(content)