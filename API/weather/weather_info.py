from datetime import datetime
from utils.logger import setup_logger
from API.weather.weather import WeatherService

logger = setup_logger("OpenLock")

class WeatherInfo:
    def real_time_info(self) -> dict:
        """
        获取实时天气信息
        """
        info = {}
        real_time_weather_alert = WeatherService().real_time_weather_alert()
        real_time_air_quality = WeatherService().real_time_air_quality()
        #解析实时天气预警
        info["obstime"] = datetime.fromisoformat(real_time_weather_alert["now"]["obsTime"]).strftime("%Y-%m-%d %H:%M")
        info["temp"] = real_time_weather_alert["now"]["temp"]    #温度
        info["feelsLike"] = real_time_weather_alert["now"]["feelsLike"]  #体感温度
        info["text"] = real_time_weather_alert["now"]["text"]    #天气情况
        info["windDir"] = real_time_weather_alert["now"]["windDir"]  #风向
        info["windScale"] = real_time_weather_alert["now"]["windScale"]  #风力等级
        info["humidity"] = real_time_weather_alert["now"]["humidity"]    #相对湿度
        info["precip"] = real_time_weather_alert["now"]["precip"]    #过去1小时降水量
        info["vis"] = real_time_weather_alert["now"]["vis"]      #能见度
        info["cloud"] = real_time_weather_alert["now"]["cloud"]      #云量
        info["pressure"] = real_time_weather_alert["now"]["pressure"] #气压

        #解析实时空气质量报告
        info["aqi"] = real_time_air_quality["indexes"][0]["aqi"]       #空气质量指数的值
        info["health_effect"] = real_time_air_quality["indexes"][0]["health"]["effect"]     #空气质量对健康的影响
        info["health_advice_general"] = real_time_air_quality["indexes"][0]["health"]["advice"]["generalPopulation"]        #对一般人群的健康指导意见
        info["health_advice_sensitive"] = real_time_air_quality["indexes"][0]["health"]["advice"]["sensitivePopulation"]        #对敏感人群的健康指导意见

        logger.info(f"成功获取实时天气信息")
        return info
    def today_info(self) -> dict:
        """
        获取每日天气信息
        """
        info = {}
        daily_weather_alert = WeatherService().daily_weather_alert()
        daily_air_quality = WeatherService().daily_air_quality()
        #解析每日天气预报
        info["updateTime"] = datetime.fromisoformat(daily_weather_alert["updateTime"]).strftime("%Y-%m-%d %H:%M")  #最近更新时间
        daily = daily_weather_alert["daily"][0] #获取今日天气预报信息
        info["sunrise"] = daily["sunrise"]  #日出时间
        info["sunset"] = daily["sunset"]    #日落时间
        info["moonPhase"] = daily["moonPhase"]  #月相名称
        info["tempMax"] = daily["tempMax"]  #预报当天最高温度
        info["tempMin"] = daily["tempMin"]  #预报当天最低温度
        info["textDay"] = daily["textDay"]  #预报白天天气状况
        info["textNight"] = daily["textNight"]  #预报晚间天气状况
        info["windDirDay"] = daily["windDirDay"]  #预报白天风向
        info["windScaleDay"] = daily["windScaleDay"]    #预报白天风力等级
        info["windDirNight"] = daily["windDirNight"]    #预报夜间当天风向
        info["windScaleNight"] = daily["windScaleNight"] #预报夜间风力等级
        info["uvIndex"] = daily["uvIndex"]  #紫外线强度指数
        info["humidity"] = daily["humidity"]    #相对湿度，百分比数值
        info["vis"] = daily["vis"]  #能见度，默认单位：公里
        #解析空气质量每日预报
        days = daily_air_quality["days"][0]["indexes"][0] #获取今日天气质量预报信息
        info["aqi"] = days["aqi"] #空气质量指数的值
        info["health_effect"] = days["health"]["effect"] #空气质量对健康的影响
        info["primaryPollutant"] = days["primaryPollutant"]["fullName"]
        info["health_advice_general"] = days["health"]["advice"]["generalPopulation"] #对一般人群的健康指导意见
        info["health_advice_sensitive"] = days["health"]["advice"]["sensitivePopulation"] #对敏感人群的健康指导意见

        logger.info("成功获取今日天气信息")
        return info

    def weather_disaster_info(self) -> dict:
        """
        获取灾害天气预警信息
        """
        info = {}
        #解析天气灾害预警
        weather_disaster_warning = WeatherService().weather_disaster_warning()

        info["updateTime"] = datetime.fromisoformat(weather_disaster_warning["updateTime"]).strftime("%Y-%m-%d %H:%M")     #获取更新时间
        info["warning"] = weather_disaster_warning["warning"]       #获取预警信息，可能为空

        logger.info(f"成功获取天气灾害预警")
        return info

    def weather_index_forecast(self) -> dict:
        """
        获取天气指数信息
        """
        info = {}
        #解析天气指数信息
        weather_index_forecast = WeatherService().weather_index_forecast()

        info["updateTime"] = datetime.fromisoformat(weather_index_forecast["updateTime"]).strftime("%Y-%m-%d %H:%M") #获取更新时间
        info["daily"] = weather_index_forecast["daily"] #获取指数信息

        logger.info(f"成功获取天气指数信息")
        return info