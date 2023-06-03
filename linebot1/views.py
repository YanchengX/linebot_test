from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage


import requests
from linebot1.models import *
import time 
import random
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#時間計算
se = time.time()
yesterday = se-86400 
tmp = time.localtime(yesterday)
resulttime = time.strftime("%m.%d",tmp)

#農作物
farmurl = "https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?$top=1000&$skip=0"
res_get = requests.get(farmurl)
farmprice = res_get.json()

#天氣
weatherurl = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-CE89DD19-8D5D-4FF4-A72F-036FB3BE367C"
jso_get = requests.get(weatherurl)
weatherpredict = jso_get.json()
city = weatherpredict['records']['location']
cityname = []
for i in range(0,len(city)):
    cityname.append(city[i]['locationName'])

#抽
pictwitch = [
'https://imgur.com/jWtb9x3','https://imgur.com/ObA0tPI','https://imgur.com/g6OP13L','https://imgur.com/bYTD1wa','https://imgur.com/whXMklk','https://imgur.com/Ye2wnWa','https://imgur.com/n3Ogzgh','https://imgur.com/jIH1uah','https://imgur.com/3Dw4VUI','https://imgur.com/ZafihTV','https://imgur.com/EM1MoE0','https://imgur.com/gAmh74Y','https://imgur.com/Qm1yRpy','https://imgur.com/4Vtg6PC','https://imgur.com/o5Mk5rk','https://imgur.com/KbweST0',
'https://imgur.com/1VcbGE7','https://imgur.com/t6rRYMF','https://imgur.com/oVUNyBk','https://imgur.com/HMudanD','https://imgur.com/p941siu','https://imgur.com/i9hJn10','https://imgur.com/5dKxEyZ','https://imgur.com/Y9LormU','https://imgur.com/ngzTqlX','https://imgur.com/7qaTH88',
    ]


for i in range(0,len(pictwitch)):
    pictwitch[i] = pictwitch[i] + "".join('.jpg')

# for i in pictwitch:
#     i += "".join(".jpg")

@csrf_exempt
def callback(request):
    if request.method == 'POST':    
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        print(body)
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                name = profile.display_name
                pic_url = profile.picture_url

                #random pic
                if mtext=="抽鼠":
                    n = random.randint(0,len(pictwitch)-1)
                    image_message = ImageSendMessage(
                        original_content_url = pictwitch[n],
                        preview_image_url = pictwitch[n]
                    )
                    line_bot_api.reply_message(
                        event.reply_token,image_message
                        )                   

                #weather
                if mtext in cityname:
                    weatheroutput = ""
                    gg = dict()
                    b = weatherpredict['records']['location']

                    for i in range(0,len(b)):   #22縣市
                        if mtext == b[i]['locationName']:
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
                                transe = time.strptime(timestre, "%Y-%m-%d %H:%M:%S")
                                resulte = time.strftime("%m-%d %H:%M", transe)
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

                    line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text=weatheroutput)
                        )

                #farmprice
                if mtext[0] == "查" and mtext[1] == " ":
                    sumstr = ""
                    for i in farmprice:
                        if resulttime in i["交易日期"]:
                            if i["作物名稱"] != None:
                                if mtext[2:] in i["作物名稱"] or mtext[2:] == i["作物名稱"]:
                                    sumstr = sumstr + "".join("作物 : %s \n"%(i["作物名稱"]))
                                    sumstr = sumstr + "".join("市場 : %s \n"%(i["市場名稱"]))
                                    sumstr = sumstr + "".join("上價 : %s \n"%(i["上價"]))
                                    sumstr = sumstr + "".join("中價 : %s \n"%(i["中價"]))
                                    sumstr = sumstr + "".join("下價 : %s \n"%(i["下價"]))
                    if sumstr != "":
                        sumstr = sumstr + "%s行情\n"%(resulttime)
                    else:
                        sumstr = "查不到"
                    line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text=sumstr)
                    )
                
                #database_user_info
                if mtext == "createmember":
                    if User_Info.objects.filter(uid=uid).exists()==False:
                        User_Info.objects.create(uid=uid,name = name,pic_url=pic_url,mtext = mtext)
                        line_bot_api.reply_message(
                            event.reply_token,TextSendMessage(text="member新增完成")
                        )
                    elif User_Info.objects.filter(uid=uid).exists()==True:
                        reply_arr = []
                        user_info = User_Info.objects.filter(uid=uid)
                        nam = ""
                        for user in user_info:
                            info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.mdt)
                            nam = user.name

                        reply_arr.append(TextSendMessage(text=info))
                        reply_arr.append(TextSendMessage("you are a member already %s"%(nam)))
                        line_bot_api.reply_message(
                            event.reply_token,reply_arr
                        )
                elif mtext == "searchmember":
                    if User_Info.objects.filter(uid=uid).exists()==True:
                        user_info = User_Info.objects.filter(uid=uid)
                        nam = ""
                        for user in user_info:
                            info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.mdt)
                            nam = user.name
                        line_bot_api.reply_message(
                            event.reply_token,TextSendMessage(text="you are a member already %s"%(nam))
                            )
                    else:
                           line_bot_api.reply_message(
                               event.reply_token,TextSendMessage(text="your aren't the member yet,if you want please text _ createmember _")
                           )                  
                 

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

        