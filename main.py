# -*-coding:utf-8-*-

import csv
import os

import requests
from bs4 import BeautifulSoup


header = {
":authority": "www.youtube.com",
":method": "GET",
":path": "/channel/UCv73CiCVYiJMjwNPsYCuOaA",
":scheme": "https",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"cache-control": "max-age=0",
"cookie": "SID=RwS1dMmROasu_LnzxnxrQdxKkuPCRc58YtWhc6YRKZnriBAgaEEdUMgX3qz2bm-rgC8VwQ.; HSID=AHunDTbBqg99rRAO2; SSID=AFb9hAuj4kkB_xenm; APISID=t5bKcfSk9bfnSZLH/AJhue4PIk86Mxx6zs; SAPISID=eoqDH4tGpaKblkmf/A8KUcosQnOr6k5z4V; VISITOR_INFO1_LIVE=l6CJ16XkcQo; PREF=f4=4000000&al=en&f1=50000000; YSC=edpyO3Ymv6I; LOGIN_INFO=AFmmF2swRQIgCO6XtN-IFoctFASSB8rZyhU0Z7aRSP-4icJzx4YEBBECIQDpXFYWQnzuL9nmOApY5IF1CyveoClz3ZcbxFHSWbTzQQ:QUQ3MjNmd1ZIT0RGeWlGR2kxUUFSWlo5RHFFR2RlNVEzakhiU0t4V3NIYXBUMVUtd0w0cHE5T3kxTVZmU2JuME9ZR1NJY3FFTzd0ZnpnNVBKZnhCeVNscmtvVkRnb1oxN2lqeS1RWGFRYk5JQ2ppNU5QSWNxMnR5MkcyTFV6a0c5RGpBYmVDXzgycUJWejRCNXdBT0NBdktSS2ZTUFNWUnRyb09qb1IyWkY5TzNEYkxvMmdWczc0",
"upgrade-insecure-requests": 1,
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3472.3 Safari/537.36",
"x-client-data": "CIe2yQEIo7bJAQisncoBCNidygEI2Z3KAQiDpMoBCOClygE=",
}


def request_html(url):
    r = requests.get(url)
    return r.content

def prase_html(html):
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    channel = soup.body.find(attrs={"class":'spf-link branded-page-header-title-link yt-uix-sessionlink'}).get_text()
    subscribers = soup.body.find(attrs={"class":"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"}).get_text()
    data = {
    'channel':channel,
    'subscribers':subscribers,
    }

    related_channels_raw = soup.body.find_all(attrs={"class":"yt-lockup-title "})
    related_channels_urls =list(filter(lambda x: 'channel' in x, list(map(lambda x:x.a['href'], related_channels_raw))))
    related_channel_ids = list(map(lambda x:x.replace('/channel/',''),related_channels_urls))

    return data, related_channel_ids

def write_csv(data):
    fname = 'youtube_channels.csv'
    fieldnames = ['id', 'channel', 'subscribers']

    if not os.path.isfile(fname):
        with open(fname,'w') as f:

            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()

    with open(fname,'a') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writerow(data)

def scraper_unit(id):
    url = "https://www.youtube.com/channel/" + id
    html = request_html(url)
    # with open('test.html','wb') as f:
    #     f.write(html)
    # html = open('test.html').read()
    data, related_channels = prase_html(html)
    data['id'] = id
    print(data)
    write_csv(data)
    return related_channels

def main():
    id = "UCv73CiCVYiJMjwNPsYCuOaA"
    related_channels = scraper_unit(id)
    for channel_id in related_channels:
        related_channels = scraper_unit(channel_id)

if __name__=='__main__':
    main()

