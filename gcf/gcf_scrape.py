#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
from time import *

import requests
import bs4
import pandas as pd


def scrape_radio_list(deep_update=False):
    """
    机核Radio各期节目URL抓取
    """
    if deep_update:
        print("机核Gadio数据重载...")
    else:
        print("正在询问机核Gadio是否有新内容...")
    pre_url = 'http://www.g-cores.com/categories/9/originals?page='
    page_num = 1
    radio_disc = {'radio_index': '',
                  'radio_title': '',
                  'radio_url': ''}
    path = os.path.dirname(__file__) + '/gcf_data.csv'
    gcf_data = pd.read_csv(path, encoding='utf-8')
    while page_num != 0:
        url = pre_url + str(page_num)
        page = requests.get(url).content
        soup = bs4.BeautifulSoup(page, "html.parser")
        radio_cases = soup.find_all('div', class_='showcase')
        if len(radio_cases) == 0:
            print('Gadio数据重载完毕')
            break
        else:
            print '取得Gadio页面数据', str(page_num), '...'
        page_num += 1
        for i in radio_cases:
            showcase_time = i.find('div', class_='showcase_time')
            radio_index = showcase_time.get_text()
            radio_index = re.sub(r'\s*\n+\s*', '\n', radio_index).strip()
            radio_index = radio_index.split('\n')
            showcase_text = i.find('div', class_='showcase_text')
            radio_title = showcase_text.find('h4').get_text()
            radio_title = radio_title.strip()
            radio_url = showcase_text.find('a').get('href')
            if not (gcf_data['radio_url'] == radio_url).any():
                radio_disc['radio_index'] = radio_index[0] +\
                    ': ' +\
                    radio_index[1]
                radio_disc['radio_program'] = radio_index[0]
                radio_disc['program_index'] = radio_index[1]
                radio_disc['radio_date'] = radio_index[-1]
                time_stamp = mktime(strptime(radio_index[-1], "%Y-%m-%d"))
                radio_disc['time_stamp'] = time_stamp
                radio_disc['radio_title'] = radio_title
                radio_disc['radio_url'] = radio_url
                radio_disc.update(scrape_radio_info(radio_url))
                gcf_data = gcf_data.append(radio_disc, ignore_index=True)
                print(u'更新节目： ' + radio_title).encode('utf-8')
            elif deep_update:
                sleep(1)
                pass
            else:
                page_num = 0
                break
    gcf_data = gcf_data.sort_values(by=['radio_date'], ascending=False)
    gcf_data.reset_index(drop=True, inplace=True)
    gcf_data.to_csv(path, encoding='utf-8', index=False)
    print('Misson Complete!')
    return


def scrape_radio_info(vol_url):
    radio_disc = {}
    page = ''
    while page == '':
        try:
            page = requests.get(vol_url).content
        except requests.exceptions.ConnectionError:
            pass
    soup = bs4.BeautifulSoup(page, "html.parser")
    djs = soup.find('div', class_='story_djs_items')
    try:
        radio_djs = [x.get_text().strip() for x in djs.find_all('a')]
        radio_djss = '###'.join(radio_djs)
    except AttributeError:
        radio_djs = []
        radio_djss = ''
    try:
        cover = soup.find('div', class_='swiper-slide')
    except AttributeError:
        cover = ''
    try:
        radio_img = cover.find('img', class_='img-responsive').get('src')
    except AttributeError:
        radio_img = ''
    radio_mp3 = soup.find('p', 'story_actions').find('a').get('href')
    radio_disc['radio_url'] = vol_url
    radio_disc['radio_dj'] = radio_djss
    radio_disc['radio_img'] = radio_img
    radio_disc['radio_mp3'] = radio_mp3
    return radio_disc


def drop_raido():
    path = os.path.dirname(__file__) + '/gcf_data.csv'
    gcf_data = pd.read_csv(path, encoding='utf-8')
    gcf_data = gcf_data.iloc[0:0]
    gcf_data.to_csv(path, encoding='utf-8', index=False)
    return


def main():
    scrape_radio_list()
    return


if __name__ == '__main__':
    main()
