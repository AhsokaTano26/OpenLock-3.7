import requests
from datetime import datetime
from API.Acode import Adcode
from utils.logger import setup_logger

logger = setup_logger("OpenLock")

old_data = {
	"code": "200",
	"location": [{
		"name": "重庆",
		"id": "101040100",
		"lat": "29.56376",
		"lon": "106.55046"
	}],
}

class WeatherService:
    def get_city_info(self):
        acode = Adcode.Acode().get_city_adcode
        code = acode()['adcode']

        url = "https://nf3qqqd5cr.re.qweatherapi.com//geo/v2/city/lookup"
        params = {"location": f"{code}"}
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"成功获取城市信息")

        except requests.exceptions.RequestException as e:
            logger.error(f"获取城市信息时出错: {e}")
            logger.info(f"使用默认配置")
            data = old_data
        except KeyError as e:
            logger.error(f"解析城市数据时出错，缺少关键字段: {e}")
            data = old_data

        city_name = data['location'][0]['name']
        city_id = data['location'][0]['id']
        dic = {}
        dic['city_name'] = city_name
        dic['city_id'] = city_id
        logger.info(f"成功获取城市信息： {city_name}-{city_id}")
        return data


    def real_time_weather_alert(self):
        get_city_id = self.get_city_info()
        id = get_city_id['location'][0]['id']
        names = get_city_id['location'][0]['name']

        url = "https://nf3qqqd5cr.re.qweatherapi.com/v7/weather/now"
        params = {"location": f"{id}"}
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            logger.info(f"获取实时天气数据成功")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"获取实时天气信息时出错: {e}")
            return f"获取实时天气信息时出错: {e}"
        except KeyError as e:
            logger.error(f"解析实时天气数据时出错，缺少关键字段: {e}")
            return f"解析实时天气数据时出错，缺少关键字段: {e}"

    def daily_weather_alert(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/v7/weather/3d"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        params = {"location": f"{lon},{lat}",}
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取每日天气预报数据错误：{e}")

    def real_time_air_quality(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/airquality/v1/current/{lat}/{lon}"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        try:
            response = requests.get(url,headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取实时空气质量数据错误：{e}")

    def hourly_air_quality(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/airquality/v1/hourly/{lat}/{lon}"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取空气质量小时预报数据错误：{e}")

    def daily_air_quality(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/airquality/v1/daily/{lat}/{lon}"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取空气质量每日预报数据错误：{e}")

    def weather_index_forecast(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/v7/indices/1d"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        params = {"location": f"{lon},{lat}",
                  "type": "0"
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取天气指数预报数据错误：{e}")

    def weather_disaster_warning(self):
        info = self.get_city_info()
        lat = info['location'][0]['lat']
        lon = info['location'][0]['lon']
        url = f"https://nf3qqqd5cr.re.qweatherapi.com/v7/warning/now"
        headers = {
            "X-QW-Api-Key": "37b3b7622980425aa3701ccda8b73078"
        }
        params = {"location": f"{lon},{lat}",}
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取天气灾害预警数据错误：{e}")