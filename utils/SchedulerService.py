from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from API.weather.weather_text import WeatherText
from API.notification.notification import NotificationService
from utils.logger import setup_logger
from data.Database.models_method import UserManager, WeatherDisasterManager

logger = setup_logger("OpenLock")

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}

        # 设置事件监听
        self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def job_listener(self, event):
        """任务执行监听器"""
        if event.exception:
            logger.error(f"定时任务 {event.job_id} 执行失败: {event.exception}")
        else:
            logger.debug(f"定时任务 {event.job_id} 执行成功")

    def add_daily_weather_check(self, hour=7, minute=0):
        """添加灾害天气检查任务"""
        job_id = "daily_weather_check"
        trigger = CronTrigger(hour=hour, minute=minute)

        self.jobs[job_id] = self.scheduler.add_job(
            self._check_daily_weather,
            trigger=trigger,
            id=job_id,
            name="灾害天气检查",
            replace_existing=True
        )
        logger.info(f"已添加灾害天气检查任务，时间: {hour:02d}:{minute:02d}")

    def _check_daily_weather(self):
        """灾害天气检查任务"""
        logger.info("执行灾害天气检查任务")
        msg = f"灾害天气提醒（{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}）"
        try:
            weather_disaster = WeatherText().weather_disaster_text()
            if weather_disaster is not None:
                msg += "\n请注意，" + weather_disaster[0]['sender_text'] + "："
                for i in weather_disaster:
                    id = i['id']
                    msg += f"{i['title']},"
                    try:
                        WeatherDisasterManager().create_new_weather_disaster(
                            id=id
                        )
                        logger.info(f"灾害天气id: {id} 写入成功")
                    except Exception as e:
                        logger.error(f"灾害天气id: {id} 写入失败：{e}")
                msg = msg[:-1]

                user_name = UserManager().get_all_user_name()
                for user in user_name:
                    user_info = UserManager().get_info_by_user_name(user)
                    if user_info.relationship in ["admin", "family"]:
                        mail_list = [user_info.mailbox]
                        NotificationService().mail_send_text(text=msg,mail_list=mail_list)
                return True
        except Exception as e:
            logger.error(f"灾害天气检查任务运行错误：{e}")
            return False

    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("定时任务调度器已启动")

            # 立即执行一次健康检查
            self.scheduler.add_job(
                self._check_daily_weather,
                'date',
                run_date=datetime.now(),
                id='initial_health_check'
            )