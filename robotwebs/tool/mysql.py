from datetime import datetime

import pymysql

from robotwebs import settings

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
    def get_info_release_time(num=50):
        '''
        获取最近50条文章的时间集合，把最旧的时间作为时间底线。（避免漏爬）
        获取时间底线（只爬取时间底线以上的文章。）
        :return:
        '''
        conn = MysqlTool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "select info_release_time from information order by info_record_time desc limit %s", num
        )
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_limit_info_release_time(time):
        '''
        获取最近50条文章的时间集合，把最旧的时间作为时间底线。（避免漏爬）
        获取时间底线（只爬取时间底线以上的文章。）
        :return:
        '''
        conn = MysqlTool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'select info_release_time from information where info_record_time > %s', time
        )
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def tuple_tuple_to_list(tuples):
        list = []
        if len(tuples) > 0:
            for tuple in tuples:
                for time in tuple:
                    list.append(time)
        return list

    @staticmethod
    def date_list_str_to_date(list, datetime_format):
        index = len(list)
        i = 0
        while i < index:
            if isinstance(list[i], str):
                list[i] = datetime.strptime(list[i], datetime_format)
            i = i + 1
        return list
