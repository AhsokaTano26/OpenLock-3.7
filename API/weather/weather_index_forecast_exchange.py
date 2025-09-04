from typing import Optional


class WeatherIndexForecastExchange():
    def exchange(self,item) -> Optional[str]:
        """将天气指数代码转换为代号"""
        Forecast = {
                "SPT": '1',
                "CW": '2',
                "DRSG": '3',
                "FIS": '4',
                "UV": '5',
                "TRA": '6',
                "AG": '7',
                "COMF": '8',
                "FLU": '9',
                "AP": '10',
                "AC": '11',
                "GL": '12',
                "MU": '13',
                "DC": '14',
                "PTFC": '15',
                "SPI": '16'
            }
        try:
            id = str(Forecast[item])
            return id
        except:
            return None