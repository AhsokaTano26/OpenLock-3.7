import requests
import re
from utils.logger import setup_logger
from config.settings import Config

logger = setup_logger("OpenLock")

amap_key = Config().get("amap_key")
ip_url = Config().get("ip_url")
location_url = Config().get("ip_location_url")

class Acode:
    def get_city_adcode(self) -> dict:
        # 步骤1: 获取公网IP地址
        try:
            ip_response = requests.get(ip_url, timeout=5)
            ip_data = ip_response.json()
            public_ip = ip_data['data']['ip']
            pattern = re.compile('\\d+\\.\\d+\\.\\d+\\.\\d+')
            matches = re.findall(pattern, public_ip)
            try:
                public_ip = matches[0]
                logger.info(f"获取公网ip成功：{public_ip}")
            except:
                logger.error(f"获取公网ip非ipv4: {public_ip}")
                public_ip = 0
        except:
            logger.error(f"获取公网ip失败")
            public_ip = 0

        # 步骤2: 使用高德地图IP定位API（需要申请API key）

        # IP定位获取城市信息
        if public_ip != 0:
            ip_location_url = f"{location_url}?ip={public_ip}&output=JSON&key={amap_key}"
        else:
            ip_location_url = f"{location_url}?output=JSON&key={amap_key}"

        try:
            location_response = requests.get(ip_location_url, timeout=5)
            location_data = location_response.json()

            if location_data['status'] == '1':
                city = location_data.get('city', '')
                province = location_data.get('province', '')
                adcode = location_data['adcode']

                logger.info(f"IP定位API请求成功")
                return {
                    'province': province,
                    'city': city,
                    'adcode': adcode,
                }

            else:
                logger.error(f"IP定位API请求失败")
                return {"error": "IP定位API请求失败"}
        except Exception as e:
            logger.error(f"请求异常: {str(e)}")
            return {"error": f"请求异常: {str(e)}"}