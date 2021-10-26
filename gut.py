# -*- coding: UTF-8 -*-
import urllib2
import re
import pandas as pd


def download(y, m, end_y, end_m):
    table = pd.DataFrame(columns=['主题', '杂志', '时间', '文章名','简介'])
    while y >= 16:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        if m < 10:
            M = '0' + str(m)
        else:
            M = str(m)
        url = 'https://www.mr-gut.cn/daily/index/1/20' + str(y) + '-' + M + '?kf=daily_last'
        urls = urllib2.Request(url, headers=send_headers)
        html = urllib2.urlopen(urls)
        html_Doc = html.read()
        html.close()
        links = re.findall(r"(<a class=\"gut-card\" href=.*target=\"_blank\">)", html_Doc)
        for k in range(0, len(links)):
            if links[k]:
                link = 'https://www.mr-gut.cn' + links[k].replace("<a class=\"gut-card\" href=\"", "").replace(
                    "\" target=\"_blank\">", "")
                urls = urllib2.Request(link, headers=send_headers)
                HTML = urllib2.urlopen(urls)
                html_Doc = HTML.read()
                HTML.close()
                title = re.findall(r"(<p class=\"rxc-daily-list-title\">.*<\/p>)", html_Doc)
                magazine = re.findall(r"(<em>.*<\/em>)", html_Doc)
                time = re.findall(r"(<div class=\"rxc-daily-list-doi\">[0-9-]*)", html_Doc)
                html = html_Doc.replace("】</a>", "")
                name = re.findall(r"(<a class=\"rxc-daily-list-blue\".*<\/a>)", html)
                section = re.findall(r"(<div class=\"rxc-daily-list\">.*?<div class=\"rxc-button-foot\">)", html_Doc, re.S)
                description = re.findall(r"(<div class=\"rxc-daily-list-desc\">.*?<\/div>)", html_Doc, re.S)
                for i in range(0, len(title)):
                    if title[i]:
                        title1 = title[i].replace("<p class=\"rxc-daily-list-title\">", "").replace("</p>", "")
                        if magazine:
                            magazine1 = magazine[i].replace("<em>", "").replace("</em>", "")
                        else:
                            magazine1 = ''
                        if time:
                            if len(title) != len(time):
                                if re.findall(r"(<div class=\"rxc-daily-list-doi\">)", section[i]):
                                    time1 = time[i].replace("<div class=\"rxc-daily-list-doi\">", "")
                                else:
                                    time1 = ''
                                    time.insert(i, '')
                            else:
                                time1 = time[i].replace("<div class=\"rxc-daily-list-doi\">", "")
                        else:
                            time1 = ''
                        if name:
                            name1 = re.findall(r"(target=\"_blank\">.*<\/a>)", name[i])
                        else:
                            name1 = ''
                        if description:
                            if len(title) != len(description):
                                if re.findall(r"(<div class=\"rxc-daily-list-desc\">)", section[i]):
                                    description1 = description[i].replace("<div class=\"rxc-daily-list-desc\">", '').replace('</div>', '').replace('\n','')
                                else:
                                    description1 = ''
                                    description.insert(i, '')
                            else:
                                description1 = description[i].replace("<div class=\"rxc-daily-list-desc\">",
                                                                      '').replace('</div>', '').replace('\n','')
                        else:
                            description1 = ''
                        for j in range(0, len(name1)):
                            if name1[j]:
                                name2 = name1[j].replace("target=\"_blank\">", "").replace("</a>", "")
                                table = table.append({'主题': title1, '杂志': magazine1, '时间': time1, '文章名': name2, '简介':description1},
                                                     ignore_index=True)
                                #print table
        print y,m
        m = m-1
        if m < 1:
            m = 12
            y = y-1
        if y == end_y and m == end_m:
            print table
            table.to_csv("D:/mr-gut.csv", sep="\t", index=False)
            return table
            break



if __name__ == '__main__':
    table1 = download(21, 10, 16, 1)
