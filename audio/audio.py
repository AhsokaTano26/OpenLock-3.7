import pyttsx3
from utils.logger import setup_logger

logger = setup_logger("OpenLock")

class AudioSystem:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.is_initialized = False

    def initialize(self):
        """初始化音频系统"""
        try:
            # 初始化语音合成
            self.tts_engine = pyttsx3.init()

            self.tts_engine.setProperty('voice', 'zh')  # 开启支持中文
            self.tts_engine.setProperty('volume', 0.5)

            self.is_initialized = True
            logger.info("音频系统初始化成功")
            return True
        except Exception as e:
            logger.error(f"音频系统初始化失败: {e}")
            return False

    def speak(self,text):
        """
        通过pyttsx3进行文字转语音
        """
        self.tts_engine.setProperty('voice', 'zh')  # 开启支持中文
        rate = self.tts_engine.getProperty('rate')
        logger.info(f"当前语速：{rate}")

        self.tts_engine.setProperty('volume', 0.5)

        # 设置要说的文本
        self.tts_engine.say(str(text))
        logger.info(f"当前speak文本：{text}")

        # 运行并等待语音完成
        self.tts_engine.runAndWait()
        self.tts_engine.stop()
        logger.info("speak完毕")