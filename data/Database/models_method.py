from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from utils.logger import setup_logger
from typing import Optional

from data.Database.model import Base, User, WeatherDisaster

logger = setup_logger("OpenLock")

database_url="sqlite:///data/db.sqlite3"

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.models = Base.__subclasses__()

    def check_database_consistency(self):
        """检查数据库结构是否与模型定义一致"""
        inspector = inspect(self.engine)
        inconsistencies = []

        for model in self.models:
            table_name = model.__tablename__

            # 检查表是否存在
            if not inspector.has_table(table_name):
                inconsistencies.append(f"表 {table_name} 不存在")
                continue

            # 获取表的列信息
            columns = inspector.get_columns(table_name)
            column_names = {col['name'] for col in columns}

            # 检查模型中的每个列是否都存在
            for column_name in model.__table__.columns.keys():
                if column_name not in column_names:
                    inconsistencies.append(f"表 {table_name} 缺少列 {column_name}")

        return inconsistencies

    def update_database_schema(self):
        """更新数据库结构以匹配模型定义"""
        try:
            # 创建所有表（如果不存在）
            Base.metadata.create_all(self.engine)
            logger.info("数据库结构已更新至最新版本")
            return True
        except Exception as e:
            logger.error(f"更新数据库结构时出错: {e}")
            return False

    def initialize_database(self):
        """初始化数据库，检查并更新结构"""
        try:
            # 测试数据库连接
            with self.engine.connect():
                pass
        except OperationalError as e:
            logger.error(f"数据库连接失败: {e}")
            return False

        # 检查数据库一致性
        inconsistencies = self.check_database_consistency()

        if inconsistencies:
            logger.warning("发现数据库结构不一致:")
            for issue in inconsistencies:
                logger.warning(f"  - {issue}")

            # 更新数据库结构
            logger.info("正在更新数据库结构...")
            return self.update_database_schema()
        else:
            logger.info("数据库结构一致，无需更新")
            return True

    def get_session(self):
        """获取数据库会话"""
        return self.Session()

class UserManager:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.models = Base.__subclasses__()

    def get_session(self):
        """获取数据库会话"""
        return self.Session()

    def close_session(self):
        """关闭当前会话"""
        self.Session.remove()

    def create_new_user(self, **kwargs) -> User:
        """创建新用户数据"""
        new_user = User(**kwargs)
        session = self.get_session()
        session.add(new_user)
        session.commit()
        self.close_session()
        return new_user

    def get_all_user_name(self, **kwargs) -> set:
        """获取所有用户名"""
        session = self.get_session()
        result = session.execute(select(User.User_name))
        return {row[0] for row in result}

    def get_info_by_user_name(self, user_name: str) -> Optional[User]:
        """通过用户名获取信息"""
        session = self.get_session()
        return session.get(User, user_name)

    def delete_info_by_user_name(self, user_name: str) -> bool:
        """通过用户名删除用户信息"""
        session = self.get_session()
        usermsg = self.get_info_by_user_name(user_name)
        if usermsg:
            session.delete(usermsg)
            session.commit()
            self.close_session()
            return True
        return False

    def update_user_info(self, user_name: str, update_data: dict) -> bool:
        """更新用户信息"""
        session = self.get_session()
        user = session.query(User).filter(User.User_name == user_name).first()
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.commit()
        self.close_session()
        return True

    def check_user(self, user_name: str) -> bool:
        """查看用户是否存在"""
        session = self.get_session()
        try:
            if session.get(User, user_name) != None:
                return True
            else:
                return False
        except OperationalError:
            return False

class WeatherDisasterManager:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.models = Base.__subclasses__()

    def get_session(self):
        """获取数据库会话"""
        return self.Session()

    def close_session(self):
        """关闭当前会话"""
        self.Session.remove()

    def create_new_weather_disaster(self, **kwargs) -> WeatherDisaster:
        """创建新用户数据"""
        new_weather_disaster = WeatherDisaster(**kwargs)
        session = self.get_session()
        session.add(new_weather_disaster)
        session.commit()
        self.close_session()
        return new_weather_disaster

    def get_info_by_id(self, id: str) -> Optional[WeatherDisaster]:
        """通过用户名获取信息"""
        session = self.get_session()
        return session.get(WeatherDisaster, id)

    def check_weather_disaster(self, id: str) -> bool:
        """查看用户是否存在"""
        session = self.get_session()
        try:
            if session.get(WeatherDisaster, id) != None:
                return True
            else:
                return False
        except OperationalError:
            return False