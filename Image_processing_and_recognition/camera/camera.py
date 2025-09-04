import cv2
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger("OpenLock")

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = None
        self.is_initialized = False

    def initialize(self):
        """初始化摄像头"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            # 设置摄像头参数
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.is_initialized = True
            logger.info("摄像头初始化成功")
            return True
        except Exception as e:
            logger.error(f"摄像头初始化失败: {e}")
            return False

    def capture_frame(self):
        """捕获一帧图像"""
        if not self.is_initialized:
            if not self.initialize():
                return None, None

        ret, frame = self.camera.read()
        if not ret:
            logger.error("无法读取摄像头帧")
            return None, None

        return ret, frame

    def record_video(self, duration=10, output_dir="data/recordings"):
        """录制视频"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/video/recording_{timestamp}.avi"

            # 设置视频编码器和输出文件
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

            # 录制指定时长的视频
            start_time = datetime.now()
            while (datetime.now() - start_time).total_seconds() < duration:
                ret, frame = self.capture_frame()
                if ret:
                    out.write(frame)

            out.release()
            logger.info(f"已录制视频: {filename}")
            return filename
        except Exception as e:
            logger.error(f"录制视频失败: {e}")
            return None

    def release(self):
        """释放摄像头资源"""
        if self.camera:
            self.camera.release()
            self.is_initialized = False
            logger.info("摄像头资源已释放")