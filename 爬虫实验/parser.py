from pyquery import PyQuery as pq
import requests
from requests.exceptions import ConnectionError
import os
from multiprocessing import Pool
import datetime
import time


def get_page(url):
    if url:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        try:
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            print('connect error')
            return None
    else:
        return None


def get_index(html):
    doc = pq(html)
    items = doc('.slist .clearfix li a').items()
    for item in items:
        yield item.attr('href')


def get_real_url(url):
    if url:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        try:
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                doc = pq(response.text)
                item= doc('.view .photo-pic a img')
                print(item.attr('src'), item.attr('title'))
                return (item.attr('src'), item.attr('title'))
            return None
        except ConnectionError:
            print('connect error')
            return None


def get_image(url):
    if url:
        print('Downloading', url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return(response.content)
            return None
        except ConnectionError:
            return None
    else:
        return None


def save_to_file(content, name):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), name, 'jpg')
    # 当前目录并不是指脚本所在的目录，而是所运行脚本的目录
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
    # 判断存在重复图片


def main(offset):
    base_url = 'http://pic.netbian.com/4kdongman/'
    url = base_url + 'index_{}.html'.format(str(offset))
    html = get_page(url)
    #print(html)
    if html:
        image_urls = get_index(html)
        for url in image_urls:
            real_url = 'http://pic.netbian.com' + url
            print(real_url)
            result = get_real_url(real_url)
            target_url = result[0]
            name = result[1]
            target_url = 'http://pic.netbian.com/' + str(target_url)
            if target_url:
                content = get_image(target_url)
                save_to_file(content, name)


if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i for i in range(2,4)])
    # pool.close()
    # pool.join()
    oldtime=datetime.datetime.now()
    main(2)
    newtime=datetime.datetime.now()
    print('程序运行时间：%s'%(newtime-oldtime))
