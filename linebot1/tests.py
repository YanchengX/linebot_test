# from urllib import request
# from wsgiref.util import request_uri
# from django.test import TestCase

import requests
import re
import time 
coun_iso_code = "TWN"
coviurl = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=3001&limited=%s"%(coun_iso_code)
#https://covid-19.nchc.org.tw/api.php?limited=BGD&tableID=3001
covidata = requests.get(coviurl)
print(covidata.content)


#天氣縣市查詢
weatherurl = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-CE89DD19-8D5D-4FF4-A72F-036FB3BE367C"
jso_get = requests.get(weatherurl)
weatherpredict = jso_get.json()
local = "臺中市"
weatheroutput = ""
gg = dict()
b = weatherpredict['records']['location']
for i in range(0,len(b)):   #22縣市
    if local == b[i]['locationName']:
        gg = dict(b[i])
        break

for g in range(0,3):
    for i in range(0,len(gg['weatherElement'])):
        tmp = gg['weatherElement'][i]['time'][g]
        if i == 0:
            timestr = tmp['startTime']
            trans = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            result = time.strftime("%m-%d %H:%M", trans)
            timestre = tmp['endTime']
            transe = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            resulte = time.strftime("%m-%d %H:%M", trans)
            weatheroutput += "".join("%s-%s\n"%(result,resulte))
            weatheroutput += "".join("%s\n"%(tmp['parameter']['parameterName']))
        elif i == 1:
            weatheroutput += "".join("%s %% 下雨 \n"%(tmp['parameter']['parameterName']))
        elif i == 2:
            weatheroutput += "".join("最低 %s 度\n"%(tmp['parameter']['parameterName']))
        elif i == 3:
            weatheroutput += "".join("天氣 %s \n"%(tmp['parameter']['parameterName']))
        elif i == 4:
            weatheroutput += "".join("最高 %s 度\n"%(tmp['parameter']['parameterName']))
print(weatheroutput)
    

#時間控制
for i in b:
    if local == b['locationName']:
        print(b)  
#Time
se = time.time()
yesterday = se-86400 
tmp = time.localtime(yesterday)
result = time.strftime("%m.%d",tmp)



# 農作物api查詢
url = "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?$top=1000&$skip=0"
res_get = requests.get(url)
a = res_get.json()
frname = []
c = "棗子"
# for i in a:
#     if result in i["交易日期"]:
#         if i["作物名稱"] is not None:
#             if c in i["作物名稱"]:
#                 print(i["作物名稱"])
#     "交易日期": "111.04.13",
#     "作物代號": "11",
#     "作物名稱": "椰子",
#     "市場代號": "104",
#     "市場名稱": "台北二",
#     "上價": 20.2,
#     "中價": 15.9,
#     "下價": 10.9,
#     "平均價": 15.8,
#     "交易量": 1408.0
#   },      


# # regex
# g = "查 f梨"
# regex = re.compile(r'查\s(\D{2})')
# match = regex.search(g)
# print(match.group(1))
