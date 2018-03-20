import pymysql

from robotwebs import settings
from tool.variable_settings import VariableSettings

host = settings.MYSQL_HOST
user = settings.MYSQL_USER
psd = settings.MYSQL_PASSWORD
db = settings.MYSQL_DB
port = 3306
use_unicode = True
charset = settings.MYSQL_CHARSET


class MysqlTool(object):

    @staticmethod
    def get_connection():
        return pymysql.connect(host=host, user=user, passwd=psd, db=db, port=port, use_unicode=True, charset="utf8")

    @staticmethod
    def get_info_record_time():
        conn = MysqlTool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'select info_record_time from information order by info_record_time limit 50'
        )
        result = cursor.fetchall()
        if result is not None:
            timelist = []
            VariableSettings.DEADLINE_TIME = result[0][0]
            for tuple in result:
                for time in tuple:
                    timelist.append(time)
            VariableSettings.TIME_LIST = timelist
        conn.close()



