import datetime
import zlib
import gzip
from urllib import request
import re

cookie_str = r'Cookie: sid=hugggx8t; LIVE_BUVID=9899d435d2ec7782d1253797e1b58f79; LIVE_BUVID__ckMd5=dbe3c0268b2c753c; fts=1532509458; buvid3=C0116210-9B51-48A6-8034-B37477A5A96D28942infoc; rpdid=kwimwklwqmdoskisimopw; UM_distinctid=164d5bdeaf3d4-00dc9e41b4becc-2711938-1aeaa0-164d5bdeaf46af; stardustvideo=1; im_notify_type_10117739=0; CURRENT_FNVAL=8; CURRENT_QUALITY=64; finger=edc6ecda; _dfcaptcha=e5a485665b2e669b4aecb7bbd4df558d; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; bp_t_offset_10117739=173267544886437204; DedeUserID=10117739; DedeUserID__ckMd5=897c2f65d4aec570; SESSDATA=72d5f670%2C1541778562%2C7fc59900; bili_jct=d994a41feeec33e1d448bba403cef3c8'
user_agent_str = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'


def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


# 当天 和 往前N天的弹幕地址列表
def history_dm_url_list(aid, history_days):
    history_url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}'
    today_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'
    today = datetime.date.today()
    start_day = today - datetime.timedelta(history_days)
    url_list = []
    cid_list = get_dm_cid_list(aid)
    for j in cid_list:
        for i in range(0, history_days):
            tmp = start_day + datetime.timedelta(i)
            url_list.append(history_url.format(j, tmp))
        url_list.append(today_url.format(j))
    return url_list


# 获取弹幕id列表
def get_dm_cid_list(aid):
    video_url = 'https://www.bilibili.com/video/av{}'.format(aid)
    req = request.Request(video_url)
    req.add_header('cookie', cookie_str)
    req.add_header('User-Agent', user_agent_str)
    resp = request.urlopen(req)
    try:
        content = gzip.decompress(resp.read()).decode('utf-8')
        res = r'{"cid":(.*?),"page"'
    except OSError:
        resp = request.urlopen(req)
        content = resp.read().decode('utf-8')
        res = r'"cid":(.*?),'
    cid_list = list(set(re.findall(res, content, re.S)))
    return cid_list


def get_aid_list():
    video_url = 'https://www.bilibili.com/ranking/all/0/0/30'
    req = request.Request(video_url)
    req.add_header('cookie', cookie_str)
    req.add_header('User-Agent', user_agent_str)
    resp = request.urlopen(req)
    content = resp.read().decode('utf-8')
    res = r'{"aid":"(.*?)","author"'
    aid_list = re.findall(res, content, re.S)
    return aid_list


def get_dm_content(url):
    req = request.Request(url)
    req.add_header('cookie', cookie_str)
    req.add_header('User-Agent', user_agent_str)
    resp = request.urlopen(req)
    dm_content = deflate(resp.read()).decode('utf-8')
    return dm_content

