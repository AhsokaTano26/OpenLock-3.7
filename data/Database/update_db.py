from data.Database.models_method import UserManager, DatabaseManager
from utils.logger import setup_logger

logger = setup_logger("OpenLock")


class update_db:
    def initialize(self):
        """初始化数据库"""
    def change_answer(self, answer):
        """将输入转换为数字"""
        if answer == 'Y':
            return 1
        elif answer == 'N':
            return 0
        else:
            print("错误输入，默认为N")
            return  0
    def information_write(self):
        """输入个人喜好模型"""
        User_name = str(input("请输入用户人脸识别代号："))
        full_name = str(input("请输入用户姓名：")) #姓名
        SPT = int(self.change_answer(input("是否热爱运动(Y/N)：")))    #运动指数 1
        DRSG = 1                                #穿衣指数 3
        FIS = int(self.change_answer(input("是否热爱钓鱼(Y/N)：")))    #钓鱼指数 4
        UV = int(self.change_answer(input("是否怕晒(Y/N)：")))        #紫外线指数 5
        TRA = int(self.change_answer(input("是否热爱旅游(Y/N)：")))    #旅游指数 6
        AG = int(self.change_answer(input("是否花粉过敏(Y/N)：")))     #花粉过敏指数 7
        COMF = 1                                 #舒适度指数 8
        FLU = int(self.change_answer(input("是否易感冒(Y/N)：")))      #感冒指数 9
        AP = 1                                   #空气污染扩散条件指数 10
        AC = 1                                   #空调开启指数 11
        GL = int(self.change_answer(input("是否爱戴太阳镜(Y/N)：")))    #太阳镜指数 12
        MU = int(self.change_answer(input("是否化妆(Y/N)：")))         #化妆指数 13
        DC = 1                                   #晾晒指数 14
        PTFC = int(self.change_answer(input("是否开车(Y/N)：")))            #交通指数 15
        SPI = 1                                  #防晒指数 16
        CW = PTFC                                #洗车指数 2
        if_come_late = int(self.change_answer(input("是否晚归(Y/N)："))) #是否晚归
        if_like_moonPhase = int(self.change_answer(input("是否喜欢观月(Y/N)：")))
        relationship = str(input("请输入与户主关系(admim/family/friend/neighbor)：")) #与户主关系
        mailbox = str(input("请输入邮箱地址："))    #邮箱地址
        try:
            UserManager().create_new_user(
                User_name=User_name,
                full_name=full_name,
                SPT=SPT,
                DRSG=DRSG,
                FIS=FIS,
                UV=UV,
                TRA=TRA,
                AG=AG,
                COMF=COMF,
                FLU=FLU,
                AP=AP,
                AC=AC,
                GL=GL,
                MU=MU,
                DC=DC,
                PTFC=PTFC,
                SPI=SPI,
                CW=CW,
                if_come_late=if_come_late,
                relationship=relationship,
                mailbox=mailbox,
                if_like_moonPhase=if_like_moonPhase,
            )
            logger.info(f"用户 {User_name} 数据写入成功！")
        except Exception as e:
            logger.error(f"数据写入失败：{e}")