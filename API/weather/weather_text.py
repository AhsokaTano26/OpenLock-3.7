from datetime import datetime
from typing import Optional

from utils.logger import setup_logger
from API.weather.weather_info import WeatherInfo
from API.weather.weather_index_forecast_exchange import WeatherIndexForecastExchange
from data.Database.models_method import UserManager, WeatherDisasterManager

logger = setup_logger("OpenLock")

class WeatherText:
    def get_time_of_day(self,time_str):
        # 将字符串转换为datetime对象
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
        hour = dt.hour

        # 判断时间段
        if 5 <= hour < 12:
            return "早上"
        elif 12 <= hour < 14:
            return "中午"
        elif 14 <= hour < 19:
            return "下午"
        elif 19 <= hour < 24:
            return "晚上"
        else:
            return "凌晨"

    def mail_send_text(self,name: str) -> str:
        real_time_weather_info = WeatherInfo().real_time_info()
        user_info = UserManager().get_info_by_user_name(name)
        weather_disaster = self.weather_disaster_text()

        time = str(datetime.now())
        time_of_day = self.get_time_of_day(time)
        if_susceptible = user_info.AG

        msg = f"""{user_info.full_name}{time_of_day}好：
当前温度：{real_time_weather_info["temp"]}°C (体感{real_time_weather_info["feelsLike"]}°C)
天气状况：{real_time_weather_info["text"]}
风向风力：{real_time_weather_info["windDir"]} {real_time_weather_info["windScale"]}级
湿度：{real_time_weather_info["humidity"]}%
降水量：{real_time_weather_info["precip"]}mm
能见度：{real_time_weather_info["vis"]}公里
气压：{real_time_weather_info["pressure"]}百帕 
空气质量：AQI={real_time_weather_info["aqi"]}"""
        if if_susceptible == 1:
            msg += "\n" + real_time_weather_info["health_advice_sensitive"]
        else:
            msg += "\n" + real_time_weather_info["health_advice_general"]
        if weather_disaster is not None:
            msg += "\n请注意，" + weather_disaster[0]['sender_text'] + "："
            for i in weather_disaster:
                msg += i['title']
            msg = msg[:-1]
        msg += f"\n数据更新时间：" + real_time_weather_info["obstime"]

        return msg

    def speak_text(self,name: str) -> str:
        weather_info = WeatherInfo().today_info()
        real_time_weather_info = WeatherInfo().real_time_info()
        user_info = UserManager().get_info_by_user_name(name)
        weather_disaster = self.weather_disaster_text()

        time = str(datetime.now())
        time_of_day = self.get_time_of_day(time)
        msg = f"{user_info.full_name}{time_of_day}好\n"

        if_come_late = user_info.if_come_late
        if_susceptible = user_info.AG
        if_car = user_info.PTFC

        msg += f"今日最高气温" + weather_info["tempMax"] + "摄氏度\n"
        msg += f"今日最低气温" + weather_info["tempMin"] + "摄氏度\n"
        msg += f"当前温度" + real_time_weather_info["temp"] + "°C,体感温度" +real_time_weather_info["feelsLike"]+ "°C\n"
        msg += f"白天天气为：" + weather_info['textDay'] + "\n"
        msg += f"白天有" + weather_info['windDirDay'] + weather_info['windScaleDay'] + "级\n"
        if if_come_late == 1:
            msg += f"晚间天气为：" + weather_info['textNight'] + "\n"
            msg += f"晚上有" + weather_info['windDirNight'] + weather_info['windScaleNight'] + "级\n"
        if '雨' in msg:
            msg += "今日有雨，记得带伞\n"
        if '雪' in msg:
            msg += "今日有雪，小心路滑\n"
        if int(weather_info["uvIndex"]) >= 7:
            msg += "今日紫外线较强，注意防护\n"
        if if_car == 1 and float(weather_info["vis"]) < 5:
            msg += f"能见度为" + weather_info["vis"] + "公里，注意安全\n"
        if float(weather_info['aqi']) < 100:
            msg += "今日空气质量良好\n"
        else:
            if if_susceptible == 1:
                msg += weather_info['health_advice_sensitive'] + "\n"
            else:
                msg += weather_info['health_advice_general'] + "\n"
        if weather_disaster is not None:
            msg += "请注意，" + weather_disaster[0]['sender_text'] + "："
            for i in weather_disaster:
                msg += i['title'] + ","
            msg = msg[:-1]

        return msg

    def weather_disaster_text(self) -> Optional[list]:
        list = []
        title_msg = ""
        text_mag = ""
        #weather_info = WeatherInfo().weather_disaster_info()
        weather_info = {
  "code": "200",
  "updateTime": "2023-04-03T14:20+08:00",
  "fxLink": "https://www.qweather.com/severe-weather/shanghai-101020100.html",
  "warning": [
    {
      "id": "10102010020230403103000500681616",
      "sender": "上海中心气象台",
      "pubTime": "2023-04-03T10:30+08:00",
      "title": "上海中心气象台发布大风蓝色预警[Ⅳ级/一般]",
      "startTime": "2023-04-03T10:30+08:00",
      "endTime": "2023-04-04T10:30+08:00",
      "status": "active",
      "level": "",
      "severity": "Minor",
      "severityColor": "Blue",
      "type": "1006",
      "typeName": "大风",
      "urgency": "",
      "certainty": "",
      "text": "上海中心气象台2023年04月03日10时30分发布大风蓝色预警[Ⅳ级/一般]：受江淮气旋影响，预计明天傍晚以前本市大部地区将出现6级阵风7-8级的东南大风，沿江沿海地区7级阵风8-9级，请注意防范大风对高空作业、交通出行、设施农业等的不利影响。",
      "related": ""
    }
  ],
  "refer": {
    "sources": [
      "12379"
    ],
    "license": [
      "QWeather Developers License"
    ]
  }
}
        for i in weather_info["warning"]:
            id = i["id"]
            if WeatherDisasterManager().check_weather_disaster(id):
                continue
            else:
                sender = i["sender"]
                sender_text = sender + "发布"
                title = i["title"].replace(sender_text,"")
                text = i["text"].replace(sender,"")
                title_msg += title + "\n"
                text_mag += text + "\n"
                list.append({"id": id,"sender": sender, "sender_text": sender_text, "title": title, "text": text})
        if len(weather_info["warning"]) == 0 or len(list) == 0:
            return None
        return list

    def weather_index_forecast_text(self,name: str) -> dict:
        info = {}   #储存user_info解析信息
        list = []   #储存用户确定有的天气指数代码
        msg = ""    #储存指数信息
        ex = WeatherIndexForecastExchange()
        weather_info = WeatherInfo().weather_index_forecast()
        user_info = UserManager().get_info_by_user_name(name)

        info[ex.exchange('SPT')] = user_info.SPT
        info[ex.exchange('DRSG')] = user_info.DRSG
        info[ex.exchange('FIS')] = user_info.FIS
        info[ex.exchange('UV')] = user_info.UV
        info[ex.exchange('TRA')] = user_info.TRA
        info[ex.exchange('AG')] = user_info.AG
        info[ex.exchange('COMF')] = user_info.COMF
        info[ex.exchange('FLU')] = user_info.FLU
        info[ex.exchange('AP')] = user_info.AP
        info[ex.exchange('AC')] = user_info.AC
        info[ex.exchange('GL')] = user_info.GL
        info[ex.exchange('MU')] = user_info.MU
        info[ex.exchange('DC')] = user_info.DC
        info[ex.exchange('PTFC')] = user_info.PTFC
        info[ex.exchange('SPI')] = user_info.SPI
        info[ex.exchange('CW')] = user_info.CW

        for key in info.keys():
            if info[key] == 1:
                list.append(key)

        for i in weather_info["daily"]:
            if str(i["type"]) in list:
                msg += i["text"]
                msg += "\n\n"

        return {
            "User_name": user_info.User_name,
            "full_name": user_info.full_name,
            "relationship": user_info.relationship,
            "mailbox": user_info.mailbox,
            "weather_index_forecast_text": msg

        }