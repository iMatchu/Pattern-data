import re
from urllib import request
import time
import json
import numpy as np

class Spider():
    # root_pattern = '<div style="padding: 1rem !important" class="card-body d-flex flex-column justify-content-around">([\s\S]*?)</div>'
    numberall_pattern = '<h4 class="red bold">([\s\S]*?)</h4>' #总数抓取

    freistaat_pattern = '<div id="Details([\s\S]*?)</i>' #定位到每个自由州
    freistaatname_pattern = '<h3 class="card-title text-left">([\s\S]*?)</h3>'
    freistaatnumber_pattern = '<h3 class="card-title red">([\s\S]*?)</h3>'
    
    city_pattern = '<tr id="Detail([\s\S]*?)</tr>' #定位到包含城市名和城市数量的标签
    cityname_pattern = '<td class="text-left">([\s\S]*?)</td>'
    citynumber_pattern = '<td class="red bold text-right">([\s\S]*?)</td>'
    
    # def Timers():
    #     ticks = time.time()
    #     return ticks

    #抓取整网页
    def __fetch_content(self):
        url = 'https://www.coronazaehler.de/'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
        req = request.Request(url=url, headers=headers)
            # r = request.urlopen(Spider.url)
        r = request.urlopen(req)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls
        
    #正则分析
    def __analysis(self,htmls):
        # root_html = re.findall(Spider.root_pattern,htmls)
        numberall = re.findall(Spider.numberall_pattern,htmls)
        print(numberall)

        infofreistaat = re.findall(Spider.freistaat_pattern,htmls)
        # print(infofreistaat)
        Anchorfreistaat=[]
        # Anchorcity=[]
        for detailfreistaat in infofreistaat:
            freistaatname = re.findall(Spider.freistaatname_pattern,detailfreistaat)
            freistaatnumber = re.findall(Spider.freistaatnumber_pattern,detailfreistaat)
            infocity = re.findall(Spider.city_pattern,detailfreistaat)
            Anchor= [freistaatname,freistaatnumber]
            Anchorfreistaat.append(Anchor)
            # print(infocity)
            # infocity = re.findall(Spider.city_pattern,detailfreistaat)
            for detailcity in infocity:
                cityname = re.findall(Spider.cityname_pattern,detailcity)
                citynumber = re.findall(Spider.citynumber_pattern,detailcity)
                Anchor1= [cityname,citynumber]
                Anchorfreistaat.append(Anchor1)
                # Anchorcity.append(Anchor1)
        # Anchorfreistaat=np.vstack(Anchorfreistaat)
        # print(Anchorfreistaat)
        return Anchorfreistaat

    #写入数据到json
    def __writedata(self,Anchorfreistaat):
        jsObj = json.dumps(Anchorfreistaat)

        fileObject = open('jsonFile.json', 'w')
        fileObject.write(jsObj)
        fileObject.close()
        # fileObject = open('sampleList.txt', 'a')
        # for ip in Anchorfreistaat:
        #     fileObject.write(ip)
        #     fileObject.write('\n')
        # fileObject.close()

    def go(self):
        htmls = self.__fetch_content()
        Anchorfreistaat=self.__analysis(htmls)
        self.__writedata(Anchorfreistaat)


    

spider = Spider()
spider.go()
