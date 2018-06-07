# -*- coding: utf-8 -*-
import os
import requests
from django.utils import encoding
from django.http import HttpResponseRedirect

MAX_PAGES = 4
SEARCH_WEB_PAGE = 'https://www.elitetorrent.biz/serie/page/'
DOWNLOAD_URL = 'https://www.elitetorrent.biz/wp-content/uploads/files/'
PARSER_STRING = '<a href="https://www.elitetorrent.biz/series/'

RSS_PATH = 'rss/static/elitetorrent.rss'

def Index(request):

    if os.path.exists(RSS_PATH):
        os.remove(RSS_PATH)

    f = open(RSS_PATH, 'w')
    f.write('<rss xmlns:tv="http://showrss.info" version="2.0">\n')
    f.write('<channel>\n')
    f.write('<title>Aresgo RSS</title>\n')
    f.write('<link>http://aresgo.ddns.net</link>\n')
    f.write('<ttl>30</ttl>\n')
    f.write('<description>RSS personal feed</description>\n')

    for page in range(1, MAX_PAGES + 1):
        request = requests.get(SEARCH_WEB_PAGE + str(page) + '/')
        if request.status_code == 200:
            for line in request.content.split('\n'):
                if PARSER_STRING in line:
                    title = line[len(PARSER_STRING):].split('/')[0]
                    url = DOWNLOAD_URL + title + '.torrent'
                    f.write('<item>\n')
                    f.write(' <title>' + title + '</title>\n')
                    f.write(' <link>' + url +'</link>\n')
                    f.write('</item>\n')

    f.write('</channel>\n')
    f.write('</rss>\n')
    f.close()

    return HttpResponseRedirect('/static/elitetorrent.rss')
