#!/usr/bin/env python
# coding: utf-8
"""
@oringin author: maidres
version 0.1
"""
__author__ = 'maidres'


import os
import requests
import re
from bs4 import BeautifulSoup

path = r'D:\Works\Code\Python\JAV\test'
#url = "https://www.javbus.com/"
#url = "https://www.javbus.info/"
url = "https://www.busjav.net/"


wd = ''

def change_folder_name_and_download_image(avcode, path, old_folder_name):

    s = requests.Session()
    r = s.get(url + avcode)
    soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')

    # get name
    name_node = soup.find('h3')

    name = name_node.text
    print '[*] ' + name

    #change folder name
    old_wd = os.path.join(path, old_folder_name)
    new_wd = os.path.join(path, name)
    os.rename(old_wd, new_wd)

    os.chdir(new_wd)

    print "[*] Downloading cover image"
    img_node = soup.find('a', attrs={"class": "bigImage"})

    download_image_over_socks5(img_node.get('href'))

    # sample picture
    print '[*] Downloading sample image'
    sample_node = soup.findAll('a', class_="sample-box")
    for sample in sample_node:
        sample_src = sample.get('href')
        download_image_over_socks5(sample_src)

    return  name

def download_image_over_socks5(img_src):

    #ir = requests.get(img_src, proxies=proxy)
    ir = requests.get(img_src)
    if ir.status_code == 200:
        open(img_src.split(".")[-2].split("/")[-1] +
             os.path.splitext(img_src)[1], 'wb').write(ir.content)
    print '[-] ' + img_src.split(".")[-2].split("/")[-1] + " done!"

def format_id(avcode):
    # insert '-'
    if avcode.find("-") == -1:
        i = 0
        l = list(avcode)
        for a in l:
            if a.isdigit():
                l.insert(i, '-')
                break
            i = i + 1
        if not l[0] == 'n':  # tokyohot
            avcode = ''.join(l)
    return avcode

def maid(wd):
    dirs = os.listdir(wd)                                                      #get dir name list
    print dirs
    for item in dirs:                                                          #search and rename AV folder,and download pic
        print item
        code = format_id(item)                                                 #get AV code
        change_folder_name_and_download_image(code, path, item)




if __name__ == '__main__':
   maid(path)