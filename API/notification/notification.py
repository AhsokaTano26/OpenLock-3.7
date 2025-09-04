import cv2
from email.utils import formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

from utils.logger import setup_logger
from API.weather.weather_text import WeatherText
from data.Database.models_method import UserManager
from audio.audio import AudioSystem

logger = setup_logger("OpenLock")


class NotificationService:
    def __init__(self, notification_url="1049109092@qq.com", chat_id="cfnqutqtuykebfjd"):
        self.notification_sender = notification_url
        self.chat_id = chat_id

    def get_admin_mailbox_ad(self) -> list:
        user_list = UserManager().get_all_user_name()
        mail_ad = []
        for user in user_list:
            user_info = UserManager().get_info_by_user_name(user)
            if user_info.relationship == 'admin':
                mail_ad.append(user_info.mailbox)
        if len(mail_ad) == 0:
            my_user = 'ahsoka_tano26@icloud.com'
            mail_ad.append(my_user)

        return mail_ad

    def mail_send_text(self,text: str,mail_list: list):
        try:
            for my_user in mail_list:
                msg = MIMEText(text, 'plain', 'utf-8')  # 填写邮件内容
                msg['From'] = formataddr(["OpenLock", self.notification_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msg['To'] = formataddr(["Admin", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['Subject'] = "OpenLock提醒"  # 邮件的主题，也可以说是标题

                server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
                server.login(self.notification_sender, self.chat_id)  # 括号中对应的是发件人邮箱账号、邮箱授权码
                server.sendmail(self.notification_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
                logger.info(f"向 {my_user} 发送邮件成功")
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            logger.error(f"邮件发送失败：{e}")

    def mail_send_image(self,snapshot_path, text: str, timestamp,mail_list: list):
        try:
            for my_user in mail_list:
                message = MIMEMultipart('related')
                subject = 'OpenLock提醒'
                subject += "  "
                subject += timestamp
                message['Subject'] = subject
                message['From'] = formataddr(["OpenLock", self.notification_sender])
                message['To'] = formataddr(["Admin", my_user])
                content = MIMEText(f'''
                                        <html><body><img src="cid:imageid" alt="imageid">{text}</body></html>
                                    ''', 'html', 'utf-8')
                message.attach(content)

                file = open(snapshot_path, "rb")
                img_data = file.read()
                file.close()

                img = MIMEImage(img_data)
                img.add_header('Content-ID', 'imageid')
                message.attach(img)

                server = smtplib.SMTP_SSL("smtp.qq.com", 465)
                server.login(self.notification_sender, self.chat_id)
                server.sendmail(self.notification_sender, my_user, message.as_string())
                server.quit()
                logger.info(f"向 {my_user} 发送邮件成功")
        except smtplib.SMTPException as e:
            logger.error(f"邮件发送失败: {e}")

    def send_security_alert(self,frame, reason="检测到陌生人") -> bool:
        """发送安全警报"""
        try:
            # 保存当前帧作为快照
            logger.info("发送警告信息")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_path = f"data/recordings/photos/snapshot_{timestamp}.jpg"
            cv2.imwrite(snapshot_path, frame)
            mail_list = self.get_admin_mailbox_ad()

            # 发送通知
            message = f"安全警报: {reason} 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.mail_send_image(snapshot_path,message,timestamp,mail_list)
            return True
        except Exception as e:
            logger.error(f"发送安全警报失败: {e}")
            return False

    def send_welcome_msg(self,name,frame):
        """发送欢迎信息"""
        try:
            logger.info("发送欢迎信息")
            if UserManager().check_user(name):
                user_info = UserManager().get_info_by_user_name(name)
                if user_info.relationship in ["admin", "family"] :
                    speak_text = WeatherText().speak_text(name)
                    mail_text = WeatherText().mail_send_text(name)
                    weather_index_forecast = WeatherText().weather_index_forecast_text(name)
                    mail_list = [user_info.mailbox]

                    mail_text += "\n今日天气指数"
                    mail_text += "\n" + weather_index_forecast['weather_index_forecast_text']

                    AudioSystem().speak(speak_text)
                    self.mail_send_text(text=mail_text,mail_list=mail_list)
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    speak_text = f"欢迎 {user_info.full_name} 到访"
                    message = f"请注意， {user_info.relationship} {user_info.full_name} 到访\n当前时间：{time}"
                    snapshot_path = f"data/recordings/photos/snapshot_{user_info.relationship}_{timestamp}.jpg"
                    cv2.imwrite(snapshot_path, frame)
                    mail_list = self.get_admin_mailbox_ad()

                    AudioSystem().speak(speak_text)
                    self.mail_send_image(snapshot_path=snapshot_path, text=message, timestamp=timestamp, mail_list=mail_list)
            else:
                AudioSystem().speak(f"用户 {name} 未在数据库注册")
                logger.info(f"用户 {name} 未在数据库注册")
        except Exception as e:
            logger.error(f"发送欢迎信息出错：{e}")