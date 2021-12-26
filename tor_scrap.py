#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

import re
#import requests

from pathlib import Path
Path('html_files').mkdir()

from torpy import TorClient
from bs4 import BeautifulSoup as bsoup



# use mimetypes instead?
assets = ['html', 'txt', 'js', 'css', 'php', \
            'jpg', 'png', 'svg', 'ico', 'gif']

# let's double check all the things
# some included .css, .js, etc. files could also 
# bring dependencies 

stage = []


def save(url: str):
    global stage, assets

    # requests module can be changed with https://github.com/torpyorg/torpy
    # this module doesn't require Tor installed on the system

    # setting Tor-proxy

#    proxies = {
#        'http': 'socks5h://localhost:9050',
#        'https': 'socks5h://localhost:9050'
#    }


    # setting paths

    if len(base := url.split('/')) < 4:
        fname = f'{base[2].split(".")[0]}.html'
    else:
        fname = f'html_files/{base[-1]}'


    # getting the web-page content and building the parser

    rq = requests.get(url, proxies=proxies, allow_redirects=True, timeout=50)
    if rq.status_code == 200:
        with open(fname, 'wb') as fl:
            fl.write(rq.content)
        cnt = Path(fname).read_text()
        soup = bsoup(rq.content, 'html.parser')
        for link in soup.find_all(['a', 'link'], href=True): # run with asyncio?
            l2 = l1 = link.img['src'] if link.img else link['href']
            if not l2.startswith('http'):
                l2 = l2.replace(l2, f'http://{base[2]}{l2}')
            _ = re.split(r'[?#\s]\s*', l2)[0]
            if _.startswith('http') and _ != (url and f'{url}/'):
                if (el := re.split(r'[./\s]\s*', _)[-1]) in assets:
                    cnt = cnt.replace(l1, (fn := f'html_files/{_.split("/")[-1]}'))
                    if _ not in stage:
                        rq2 = requests.get(l2, proxies=proxies)
                        with open(f'{fn}', 'wb') as asset:
                            asset.write(rq2.content)
                        stage.append(_)
        Path(fname).write_text(cnt)


# run the main function
url = 'http://cryptbb2gezhohku.onion'
print('Preparing root folder..\n')
save(url)

# Ln 16
for el in stage:
    for ext in assets[:4]:
        if el.endswith(ext):
            print(f'Link: {el}', end='\r')
            save(el)

