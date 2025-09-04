import json
import logging
from pathlib import Path


class Config:
    def __init__(self):
        self.config = {
            "camera_index": 0,
            "detection_interval": 2,
            "recognition_threshold": 0.6,
            "weather_city": "Chongqing",
            "data_dir": "data",
            "amap_key": "20220808af1c658565b70cc69d8084da",
            "ip_url": "https://api.ipify.org",
            "ip_location_url": "https://restapi.amap.com/v3/ip",
            "file_list": "data/known_faces/face_list.txt",
            "face_model": "data/known_faces/trainer.yml",
            "notification_url": "1049109092@qq.com",
            "notification_chat_id": "cfnqutqtuykebfjd"
        }

        # 创建数据目录
        Path(self.config["data_dir"]).mkdir(exist_ok=True)
        Path(f"{self.config['data_dir']}/known_faces").mkdir(exist_ok=True)
        Path(f"{self.config['data_dir']}/recordings").mkdir(exist_ok=True)
        Path(f"{self.config['data_dir']}/recordings/photos").mkdir(exist_ok=True)
        Path(f"{self.config['data_dir']}/recordings/video").mkdir(exist_ok=True)
        Path(f"{self.config['data_dir']}/models").mkdir(exist_ok=True)

        self.load_config_file()

    def load_config_file(self):
        """从文件加载配置"""
        try:
            with open("config/config.json", "r",encoding='utf-8') as f:
                file_config = json.load(f)
                self.config.update(file_config)
                logging.info("配置文件加载成功")
        except FileNotFoundError:
            logging.warning("配置文件不存在，使用默认配置")
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")

    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)

    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value

        # 保存到文件
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"保存配置失败: {e}")