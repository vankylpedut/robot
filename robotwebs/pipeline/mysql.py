import pymysql

from robotwebs import settings

host = settings.MYSQL_HOST
user = settings.MYSQL_USER
psd = settings.MYSQL_PASSWORD
db = settings.MYSQL_DB
port = 3306
use_unicode = True
charset = settings.MYSQL_CHARSET


class Mysql(object):
    @staticmethod
    def get_connection():
        return pymysql.connect(host=host, user=user, passwd=psd, db=db, port=port, use_unicode=True, charset="utf8")
