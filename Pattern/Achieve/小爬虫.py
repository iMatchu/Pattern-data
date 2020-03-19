import re
from urllib import request
import time
import json
import pandas as pd
import numpy as np

class Spider():
    # root_pattern = '<div style="padding: 1rem !important" class="card-body d-flex flex-column justify-content-around">([\s\S]*?)</div>'
    numberall_pattern = '<h4 class="red bold">([\s\S]*?)</h4>' #正则总数

    freistaat_pattern = '<div id="Details([\s\S]*?)</i>' #正则定位到包含自由州州名和数量的标签
    freistaatname_pattern = '<h4 class="card-title text-center">([\s\S]*?)</h4>'
    freistaatnumber_pattern = '<h5 class="card-title red mb-0">([\s\S]*?)</h5>'
    
    city_pattern = '<tr id="Detail([\s\S]*?)</tr>' #正则定位到包含城市名和城市数量的标签
    cityname_pattern = '<td class="text-left">([\s\S]*?)</td>'
    citynumber_pattern = '<td class="red bold text-right">([\s\S]*?)</td>'
    
    def __timers(self):
        # ticks = time.time()时间戳
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return localtime

    #抓取整网页
    def __fetch_content(self):
        url = 'https://www.coronazaehler.de/'
        #假装有个头文件,绕过反爬
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
        req = request.Request(url=url, headers=headers)
            # r = request.urlopen(Spider.url)
        r = request.urlopen(req)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls
        
    #正则分析
    def __analysis(self,htmls,localtime):
        # root_html = re.findall(Spider.root_pattern,htmls)
        numberall = re.findall(Spider.numberall_pattern,htmls) #爬总数
        # print(numberall)

        infofreistaat = re.findall(Spider.freistaat_pattern,htmls) #爬州信息
        # print(infofreistaat)
        Anchorfreistaat=[{'Name':'Deutschland', 'Number\n'+localtime:numberall}]
        # Anchorcity=[]
        for detailfreistaat in infofreistaat:                      #遍历所有州  写入字典
            freistaatname = re.findall(Spider.freistaatname_pattern,detailfreistaat)
            freistaatnumber = re.findall(Spider.freistaatnumber_pattern,detailfreistaat)
            infocity = re.findall(Spider.city_pattern,detailfreistaat)
            Anchor= {'Name':'Freistaat name '+ str(freistaatname), 'Number\n'+localtime: '+++ ' + str(freistaatnumber)+' +++'}
            Anchorfreistaat.append(Anchor)
            # print(infocity)
            # infocity = re.findall(Spider.city_pattern,detailfreistaat)
            for detailcity in infocity:                            #遍历各州下的所有城市  写入字典
                cityname = re.findall(Spider.cityname_pattern,detailcity)
                citynumber = re.findall(Spider.citynumber_pattern,detailcity)
                Anchor1= {'Name':cityname, 'Number\n'+localtime:citynumber}
                Anchorfreistaat.append(Anchor1)
                # Anchorcity.append(Anchor1)
        # Anchorfreistaat=np.vstack(Anchorfreistaat)
        # print(Anchorfreistaat)
        return Anchorfreistaat

    #使用panda将字典数据处理成矩阵   
    def __usepandas(self,Anchorfreistaat):
        Anchorfreistaat = pd.DataFrame.from_dict(Anchorfreistaat)
        # print(Anchorfreistaat.iloc[0:,1])
        print(Anchorfreistaat)
        return Anchorfreistaat
    
 
    #读取
    def __readdata(self,Anchorfreistaat):
        Anchorfreistaatold=pd.read_csv('Covidata.csv')
        #拼接数据
        Anchorfreistaat=pd.concat([Anchorfreistaatold,Anchorfreistaat.iloc[0:,1]],axis=1)
        #删除数据最后一行
        # Anchorfreistaat=Anchorfreistaatold.drop(['Number\n2020-03-19 07:48:46'],axis=1) 
        return Anchorfreistaat
        
        
    
    #输出数据到csv
    def __writedata(self,Anchorfreistaat):
        #json输出txt 按[n*1]输出
        # with open('test.txt', 'a') as file:
        #     for i in Anchorfreistaat:
        #         file.write(json.dumps(i)+'\n') 

        #np输出,输出清晰的矩阵
        # np.savetxt(r'.\test1.txt', Anchorfreistaat.values, fmt='%d')

        #输出csv
        Anchorfreistaat.to_csv(r'Covidata.csv',index = False)
        
        #写入数据到json
        # jsObj = json.dumps(Anchorfreistaat)
        # fileObject = open('jsonFile.json', 'a')
        # fileObject.write(jsObj)
        # fileObject.close()
        
        #写入txt的方法
        # fileObject = open('sampleList.txt', 'a') 
        # for ip in Anchorfreistaat:
        #     fileObject.write(ip)
        #     fileObject.write('\n')
        # fileObject.close()

    #运行
    def go(self):
        localtime=self.__timers()
        htmls = self.__fetch_content()
        Anchorfreistaat=self.__analysis(htmls,localtime)
        Anchorfreistaat=self.__usepandas(Anchorfreistaat)
        # Anchorfreistaat=self.__readdata(Anchorfreistaat)
        # self.__writedata(Anchorfreistaat)

spider = Spider()
spider.go()