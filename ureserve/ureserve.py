#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
from bs4 import BeautifulSoup

errors = []
hits = []

conn = httplib.HTTPConnection("www.ureserv.com")

def _parse_soup(htmlDoc):
	#soup = BeautifulSoup(htmlDoc, "lxml")
	soup = BeautifulSoup(htmlDoc)
	divs = soup.findAll(True, {'class': "timingTd"})
	if divs:
		div = divs[0]
		div_contents = div.contents
		if div_contents:
			content = div_contents[0]
			#option_tag = content.findAll(selected="selected")
			select_tags = content.findAll(id="where")
			if select_tags:
				select_tag = select_tags[0]
				select_tag_contents = select_tag.contents
				if select_tag_contents:
					rest_name = select_tag_contents[0].contents
					return rest_name[0]
				else:
					return None
	else:
		return None

#for i in [499]:
#for i in [1, 499]:
for i in range(1, 2001):
	route = "/index.php/Booking/Booking/widgetindex/restid/%s" % i
	conn.request("GET", route)	
	r1 = conn.getresponse()
	print "processing restau %s" % i
	if (r1.status == httplib.OK):
		html = r1.read()
		restName = _parse_soup(html)
		if restName:
			hits.append([i, restName])
	else:
		print r1.status, r1.reason
		errors.append(route) 

conn.close()

if errors:
	print "ERROR fetching data for routes:\n"
	for error in errors:
		print error

for hit in hits:
	print hit


