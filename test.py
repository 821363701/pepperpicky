__author__ = 'yu'

import requests
from BeautifulSoup import BeautifulSoup, NavigableString
from PIL import Image
from io import BytesIO

raw_cookie = 'bid="AVRekjtmmtM"; ue="doubanxiong@live.cn"; ll="108296"; JSESSIONID=aaaELGO44yuImfnEUlb9u; _ga=GA1.2.984907948.1427943741; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1440496720%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dzyk9sQSdhV1nHB1NAGgBOok_elpLXCqwTB1XeMj5yZxoy32UfgMfio2Uy6jpG1Kt-7ZHoHY0mjnrpMVp1nscXK%26wd%3D%26eqid%3Dccf418b800007a4c0000000255bb24e4%22%5D; __utmt=1; dbcl2="27729491:nXHIH9y11JA"; ck="Tmdb"; push_noty_num=2; push_doumail_num=0; _pk_id.100001.8cb4=63415abb32a1a2b2.1427943740.13.1440496732.1440493946.; _pk_ses.100001.8cb4=*; __utma=30149280.984907948.1427943741.1440491295.1440496721.15; __utmb=30149280.3.10.1440496721; __utmc=30149280; __utmz=30149280.1438328054.13.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.2772'
cookies = {}
for coo in raw_cookie.split(';'):
    try:
        d = coo.strip()
        key, value = d.split('=')
        cookies[key] = value
    except:
        pass


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
                    break
        elif item.name == 'div':
            print_beautiful(item)
        else:
            print 'unrecognized tag'



topic_url = u'http://www.douban.com/group/topic/79001001'

r = requests.get(topic_url, cookies=cookies)
soup = BeautifulSoup(r.text)
r.close()

content = soup.find('div', {'class': 'topic-content'})
print_beautiful(content)