import cv2
import time
import threading
#opencv-contrib-python
# 导入自定义模块
from config.settings import Config
from Image_processing_and_recognition.camera.camera import Camera
from audio.audio import AudioSystem
from Image_processing_and_recognition.human_detect.detect.detect import FaceRecognition
from API.weather.weather_text import WeatherText
from API.notification.notification import NotificationService
from utils.logger import setup_logger
from data.Database.update_db import update_db
from data.Database.models_method import UserManager, DatabaseManager
from utils.SchedulerService import SchedulerService
#from sensor.ultrasonic_ranging import UltrasonicRanging

file_list = Config().get("file_list")
face_model = Config().get("face_model")

logger = setup_logger("OpenLock")

class DoorGodSystem:
    def __init__(self):

        # 加载配置
        self.config = Config()

        # 初始化组件
        self.camera = Camera(self.config.get("camera_index", 0))
        self.audio = AudioSystem()
        DatabaseManager().initialize_database()
        self.face_recognition = FaceRecognition()
        self.weather_service = WeatherText()
        self.scheduler = SchedulerService()
        self.notification_service = NotificationService(
            self.config.get("notification_url"),
            self.config.get("notification_chat_id")
        )
        self.db = UserManager

        # 状态变量
        self.is_running = False
        self.last_detection_time = 0

    def setup_scheduled_tasks(self):
        """设置定时任务"""
        weather_hour = self.config.get("scheduled_tasks", {}).get("weather_check", {}).get("hour", 1)
        weather_minute = self.config.get("scheduled_tasks", {}).get("weather_check", {}).get("minute", 0)
        self.scheduler.add_daily_weather_check(hour=weather_hour, minute=weather_minute)

    def process_detection(self,flag,frame,name):
        """处理检测结果"""
        current_time = time.time()
        face_names = []
        face_names.append(name)
        # 如果是熟人，生成问候语
        if flag:
            # 避免频繁问候
            if current_time - self.last_detection_time > 300:  # 10秒内不重复问候
                self.last_detection_time = current_time

                # 发送欢迎信息
                self.notification_service.send_welcome_msg(name=name,frame=frame)

        # 如果是陌生人，录制视频并发送通知
        else:
            # 避免频繁录制
            if current_time - self.last_detection_time > 30:  # 30秒内不重复录制
                self.last_detection_time = current_time

                # 在单独线程中处理安全警报
                def security_procedure():
                    # 发送通知
                    self.notification_service.send_security_alert(frame=frame)
                    # 录制视频
                    self.camera.record_video(10, f"{self.config.get('data_dir', 'data')}/recordings")

                threading.Thread(target=security_procedure, daemon=True).start()

        return face_names

    def run(self):
        """运行主循环"""
        # 初始化摄像头
        if not self.camera.initialize():
            logger.error("无法初始化摄像头，系统退出")
            return

        # 初始化音频系统
        if not self.audio.initialize():
            logger.warning("音频系统初始化失败，部分功能受限")

        self.is_running = True
        logger.info("智能门神系统启动成功")

        # 播放启动提示音
        self.audio.speak("智能门神系统已启动")

        # 检测人脸
        dic_face = FaceRecognition().read_dic_face(file_list)
        # 加载Opencv人脸检测器
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

        # 加载训练好的人脸识别器
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(face_model)
        logger.info(f"加载字典：{dic_face}")

        # 主循环
        self.setup_scheduled_tasks()
        self.scheduler.start()
        while self.is_running:
            #UltrasonicRanging().setup()
            i = 0
            ranging = 1#UltrasonicRanging().loop(i)
            if ranging < 30:
                try:
                    # 读取摄像头帧
                    ret, frame = self.camera.capture_frame()
                    if not ret:
                        logger.error("无法读取摄像头帧")
                        time.sleep(1)
                        continue

                    # 每隔一定时间进行检测
                    current_time = time.time()
                    if current_time - self.last_detection_time > self.config.get("detection_interval", 10):
                        face_locations = self.face_recognition.face_detect(recognizer,faceCascade,dic_face,frame)

                        # 处理检测结果
                        if face_locations:
                            flag = face_locations["flag"]
                            color = face_locations["color"]
                            name = face_locations["str_face"]
                            x, y, w, h = face_locations["x"], face_locations["y"], face_locations["w"], face_locations["h"]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            self.process_detection(flag=flag,frame=frame,name=name)

                    # 显示实时画面
                    cv2.imshow('Door God System', frame)

                    # 检查键盘输入
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key  == ord('d'):
                        username = str(input("请输入删除用户姓名："))
                        if UserManager().check_user(username):
                            if UserManager().delete_info_by_user_name(username):
                                logger.info("删除成功")
                            else:
                                logger.info("删除失败")
                        else:
                            logger.debug("用户不存在")
                    elif key == ord('r'):
                        # 注册新人脸
                        update_db().information_write()
                    time.sleep(1)

                except KeyboardInterrupt:
                    logger.info("用户中断系统运行")
                    break
                except Exception as e:
                    logger.error(f"主循环错误: {e}")
                    time.sleep(1)

            #time.sleep(10)

        # 清理资源
        self.camera.release()
        cv2.destroyAllWindows()
        logger.info("智能门神系统已关闭")


if __name__ == "__main__":
    system = DoorGodSystem()
    system.run()




