#coding=utf-8

import urllib2
from lxml import etree
import datetime
import json
import random
import sys
from tkinter import scrolledtext

reload(sys)
sys.setdefaultencoding('utf-8')


# 爬取数据类
class Flight(object):

    def __init__(self, cities, dates, scr):
        # 城市
        self.cities = cities
        # 日期
        self.dates = dates
        # Log输出框
        self.scr = scr
        # 爬取数据
        self.flight = self._spider(self.cities, self.dates)

    # 保存文件
    def save(self, path='data.json'):
        with open(path, 'w+') as json_file:
            json.dump(self.flight, json_file, ensure_ascii=False)

    def _spider(self, cities, dates):
        #爬取的数据保存到字典
        flight = {}
        for city in cities:
            print(city[0] + '-' + city[1])
            if isinstance(self.scr, scrolledtext.ScrolledText):
                self.scr.insert('end', city[0] + '-' + city[1] + '\n')
            flight[city[0] + '-' + city[1]] = {}
            for date in dates:
                # 获得参数
                rk, CK, r = self._get_parameter(date)
                # 爬取某条数据
                flight[city[0] + '-' + city[1]][date] = self._get_json2(city[0], city[1], date, rk, CK, r)
            if isinstance(self.scr, scrolledtext.ScrolledText):
                self.scr.insert('end', '\n')
        if isinstance(self.scr, scrolledtext.ScrolledText):
            self.scr.insert('end', '\n')

        return flight

    def _get_json2(self, dcity, acity, date, rk, CK, r):
        url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights" \
              + "?DCity1=" + dcity + "&ACity1=" + acity + "&SearchType=S" + "&DDate1=" + date \
              + "&IsNearAirportRecommond=0" + "&rk=" + rk + "&CK=" + CK + "&r=" + r

        headers = {'Host': "flights.ctrip.com",
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   'Cookie': '_fpacid=09031171110905036232; DomesticUserHostCity=KHN|%c4%cf%b2%fd; _abtest_userid=517d042b-375f-477f-be51-84a418fa7a11; _bfa=1.1526620968644.32ldng.1.1526703272641.1526706171936.5.17; _RF1=222.204.49.211; _RSG=EwqAxDDwun30OlsohvUyX8; _RDG=2853385d068fee24ab18009b2deb3d3827; _RGUID=3c78e8d3-7b2b-4e8e-887c-7b9af2daf600; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1527225771478; _jzqco=%7C%7C%7C%7C%7C1.371278076.1526620971522.1526706416696.1526706423376.1526706416696.1526706423376.0.0.0.13.13; __zpspc=9.5.1526706175.1526706423.3%232%7Cwww.baidu.com%7C%7C%7C%7C%23; MKT_Pagesource=PC; appFloatCnt=2; _ga=GA1.2.1155635020.1526620974; _gid=GA1.2.1313887088.1526620974; FD_SearchHistorty={"type":"D","data":"D%24%u4E0A%u6D77%28SHA%29%24SHA%242018-05-19%24%u897F%u5B89%28SIA%29%24SIA%242018-05-19%24%24"}; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1526706423354%7D%5D; manualclose=1; _bfi=p1%3D10320662761%26p2%3D100101991%26v1%3D17%26v2%3D16; _bfs=1.6; login_uid=756B9CDA808F7044988F35A203523FD5; login_type=0; cticket=E2F4309CA8BF5DA3BDEDCAFACF4A8329FEA3FE4CA64349E2C487506B5A2199A8; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojZ7es+HG+PyxCQPpA6/Y4YhyG6zWyOCzizFL8n+YXgj5f+eu0OTZn6090zr1aJSniJBY0WKOXYeCzhlyH7X09bqPlffl6gwgMUTdY80y5LjNAha0GUis+PmQPCY6CW9FzT7gLLyKI9dDGEa5c5pKFqu6OlXdoX9f+BznoEPxOgw/g+a65XsQTxFY9Kd4MMf/xYqNjmMcuT7U96joubV+3odD/JZuDQwR+Cye1Pgj05HUpBxYm3TeZ2NEOfve1UA6KpT3dNubV6Vs=; AHeadUserInfo=VipGrade=0&UserName=&NoReadMessageCount=0; DUID=u=F0CA5ECB92AF1AE09B315DA09AAA21CF&v=0; IsNonUser=F; UUID=7ED54E61AC254B8CAFA8DA6D19F082E4; IsPersonalizedLogin=F',
                   'Referer': "http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s" % date}

        req = urllib2.Request(url, headers=headers)
        # 请求url
        res = urllib2.urlopen(req)
        # 获取返回结果
        content = res.read()
        dict_content = json.loads(unicode(content, 'gbk'), encoding="ISO-8859-1")
        print(date + ': ' + str(len(dict_content['fis'])))
        if isinstance(self.scr, scrolledtext.ScrolledText):
            self.scr.insert('end', date + ': ' + str(len(dict_content['fis'])) + '\n')

        # 处理返回结果
        outputs = []
        for i in range(len(dict_content['fis'])):
            if dict_content['fis'][i][u'scs'][0][u'c'] == "Y":
                dt = int(dict_content['fis'][i][u'dt'][11:13]) * 60 + int(dict_content['fis'][i][u'dt'][14:16])
                at = int(dict_content['fis'][i][u'at'][11:13]) * 60 + int(dict_content['fis'][i][u'at'][14:16])
                outputs.append([dict_content['fis'][i][u'alc'], dict_content['fis'][i][u'lp'], dt, at - dt if at - dt > 0 else at - dt + 24 * 60])

        return outputs

    def _get_parameter(self, date):
        url = 'http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s' % date
        res = urllib2.urlopen(url).read()
        tree = etree.HTML(res)
        pp = tree.xpath('''//body/script[1]/text()''')[0].split()
        CK_original = pp[3][-34:-2]
        CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]

        rk = pp[-1][18:24]
        num = random.random() * 10
        num_str = "%.15f" % num
        rk = num_str + rk
        r = pp[-1][27:len(pp[-1]) - 3]

        return rk, CK, r


# 获取某天到某天直接所有的日期字符串
def datelist(start, end):
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result


def spider(city, datestart, dataend, scr=None):
    city = eval(city)
    c = []
    for i in range(len(city) - 1):
        for j in range(i + 1, len(city)):
            c += [[city[i], city[j]]]
    flight = Flight(c, datelist(datestart, dataend), scr)

    return flight


if __name__ == '__main__':

    flight = spider("'SHA', 'SIA'", "2018-06-01", "2018-06-02")
    flight.save('out.json')
