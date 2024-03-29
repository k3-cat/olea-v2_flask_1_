import re

import requests
from bs4 import BeautifulSoup

from enums import ProjCat
from exts import redis

from .errors import InvalidSource, UnableToFetchTitle

CN_SITE_URL = 'http://scp-wiki-cn.wikidot.com'


def fetch_web(url):
    web_page = redis.get(url)
    if not web_page:
        web_page = requests.get(f'{CN_SITE_URL}/{url}').text
        redis[url] = web_page
        redis.pexpire(url, ex=180)
    soup = BeautifulSoup(web_page, 'lxml')
    return soup.find('div', {'id': 'main-content'})


def fetch_title_by_url(url):
    web = fetch_web(url)
    title_e = web.find('div', {'id': 'page-title'})
    return title_e.text.strip()


def fetch_title_by_id(url, id_):
    web = fetch_web(url)
    try:
        title_e = web.find_all(name='a', text=f'SCP-{id_}', limit=1)[0]
        if not title_e:
            raise UnableToFetchTitle()
        return str(title_e.parent)
    except IndexError:
        raise UnableToFetchTitle()


def build_basic_info(base, cat):
    if cat is not ProjCat.normal:
        title = base
        source = base
    elif base[0] == '/':
        source = base
        title = fetch_title_by_url(base)
    else:
        base = re.match(r'^(?:scp-)?(.*)$', base.lower()).group(1)
        source = f'/scp-{base}'
        title = f'SCP-{base}'.upper()
        primary = re.match(r'^(?:cn-)?([0-9]{3,4})((?:-j)|(?:-ex))?$', base)
        if primary:
            # SCP-000 SCP-000-J SCP-000-EX
            # SCP-CN-000 SCP-CN-000-J SCP-CN-000-EX
            page = 1
            if '-j' in base:
                url_ = 'joke-scps'
            elif '-ex' in base:
                url_ = 'scp-ex'
            else:
                page = int(primary.group(1)) // 1000 + 1
                url_ = 'scp-series'
            url_ += '-cn' if 'cn-' in base else ''
            url_ += f'-{page}/' if page != 1 else '/'
        elif re.match(r'^[0-9]{3,4}-jp(?:-j)?$', base):
            url_ = 'scp-international/'
        else:
            raise InvalidSource()
        raw_title = re.match('^<li><a.*/a>(.*)</li>$',
                             fetch_title_by_id(url_, base.upper()))
        title += raw_title.group(1)
    return title, source


def count_chars(text):
    text = re.sub(r'█', 'x', text.lower())
    text = re.sub(r'x  (x  )*x', 'xx', re.sub(r'[0-9a-z-]', ' x ', text))
    text = re.sub(r'(?![\u4e00-\u9fa5]|[0-9a-z-]).', ' ', text)
    str_list = re.sub(r'\s+', ' ', text).split(' ')
    count = 0
    for elem in str_list:
        if 'x' in elem:
            count += 1
        else:
            count += len(elem)
    return count


def build_complexity_info(proj):
    if proj.source[0] != '/':
        wc = 0
    else:
        web = fetch_web(proj.source)
        page_content = web.find('div', {'id': 'page-content'})
        wc = count_chars(page_content.text)
    return {'al': {}, 'cl': {}, 'wc': wc, 'vl': 0}
