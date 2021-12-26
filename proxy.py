#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-

import asyncio
import aiohttp

from aiohttp_socks import ProxyConnector


in1 = input('Proxy file-list: ')
url = 'http://ident.me'
clean = open('prx.txt', 'a')

with open(in1, 'r') as pr:
	prx = [ln.rstrip() for ln in pr]

async def start(pr: str):
	try:
		conn = ProxyConnector.from_url(f'http://{pr}')
	except ValueError:
		pass

	cnt = 0
	try:
		async with aiohttp.ClientSession(connector=conn) as session:
			async with session.get(url, timeout=2) as response:
				cnt += 1
				print(f'Proxies: {cnt} / {len(prx)}', end='\r')
				clean.write(f'{pr}\n')
	except Exception as e:
#		print(e, f'{pr}    -------')
		pass

async def main():
	await asyncio.gather(*[start(pr=pr) for pr in prx])

asyncio.run(main())

