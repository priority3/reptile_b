import requests
import time
import random
import pandas as pd
import json
import re
def get_extra(keyword:str, page:int,saveName:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': "buvid3=0840FBEE-6D20-07CF-7ED7-E25388723CAF31310infoc; b_nut=1680490831; i-wanna-go-back=-1; _uuid=3A191794-6D410-86103-26B5-8BB539A953FD32521infoc; nostalgia_conf=-1; CURRENT_FNVAL=4048; CURRENT_PID=bdea2b40-d1cb-11ed-8d66-9145f491126e; rpdid=|(J||k~u~~|Y0J'uY)|Rm|)lJ; buvid4=775F90C6-2F51-8FF4-0DCF-48DCD4B236C135148-023040311-NcaA6oyKsGNmkQN6VL%2Fw5Q%3D%3D; DedeUserID=94544300; DedeUserID__ckMd5=4d694bbe0a51cf55; SESSDATA=5b41524c%2C1696042927%2Ca765c%2A41; bili_jct=176e781085177d29239a628338b2c0fa; b_ut=5; header_theme_version=CLOSE; buvid_fp_plain=undefined; CURRENT_QUALITY=80; FEED_LIVE_VERSION=V8; home_feed_column=5; LIVE_BUVID=AUTO5016826071243014; fingerprint=ffae4707ffe7970a5d8fc9ae95a00192; buvid_fp=fc9a38a796e61cbaf2eb8a13b48a6847; browser_resolution=1920-975; PVID=3; bp_video_offset_94544300=804412172998279200; innersign=0; b_lsid=E7DBFD41_18898FA753D"
    }
    result = pd.DataFrame()
    for i in range(1, page+1):
        url = f'https://api.bilibili.com/x/web-interface/wbi/search/type?__refresh__=true&_extra=&context=&page={i}&page_size=42&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword={keyword}&qv_id=rhY003mZbHrQGXl1fXqvj8PqEhlA7eT1&ad_resource=5654&source_tag=3&gaia_vtoken=&category_id=&search_type=video&dynamic_offset=24&web_location=1430654&w_rid=30f8c59f9997002ec4e584ae3bd15d26&wts=1686194457'
        res = requests.get(url.format(i), headers=headers)
        data = json.loads(res.content.decode('utf-8'))['data']['result']
        for item in data:
            video_url = item['arcurl']
            video_author = item['author']
            video_description = item['description']
            video_typename = item['typename']
            video_tag = item['tag']
            # danmu
            video_review = item['video_review']
            # play
            video_play = item['play']
            video_duration = item['duration']
            # dianzan
            video_like = item['like']
            # shoucang
            video_favorites = item['favorites']
            video_bvid = item['bvid']
            video_pubdate = time.strftime("%Y-%m-%d", time.localtime(item['pubdate']))
            # format title "<em class=\"keyword\">王冰冰</em>直拍，这声音好听吗？"
            video_title = re.sub(r'<[^>]+>', '', item['title'])
            df = pd.DataFrame({
                'video_title': [video_title],
                'video_author': [video_author],
                'video_pubdate': [video_pubdate],
                'video_url': [video_url],
                'video_duration': [video_duration],
                'video_review': [video_review],
                'video_play': [video_play],
                'video_like': [video_like],
                'video_favorites': [video_favorites],
                'video_bvid': [video_bvid],
                'video_description': [video_description],
                'video_typename': [video_typename],
                'video_tag': [video_tag]
            })
            result = pd.concat([result, df])
        time.sleep(random.random() + 1)
        print('已经完成b站第 {} 页爬取'.format(i))
    saveName = saveName + ".csv"
    result.to_csv(saveName, encoding='utf-8-sig', index=False)
    return result
if __name__ == '__main__':
    keyword = input("请输入关键词：")
    page = int(input("请输入爬取页数："))
    saveName = input("请输入保存文件名：")
    get_extra(keyword,page,saveName)